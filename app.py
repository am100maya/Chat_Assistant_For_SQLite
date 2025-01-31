import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_openai import ChatOpenAI

st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🦜")
st.title("🦜 LangChain: Chat with SQL DB")

LOCALDB = "USE_LOCALDB"
db_uri = LOCALDB
api_key = "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"  # Ensure your API key is securely stored

## LLM model
llm = ChatOpenAI(api_key=api_key, model_name="gpt-4", streaming=True)

@st.cache_resource(ttl="2h")
def configure_db(db_uri):
    dbfilepath1 = (Path(__file__).parent / "company.db").absolute()
    creator = lambda: sqlite3.connect(f"file:{dbfilepath1}?mode=ro", uri=True)
    engine = create_engine("sqlite:///", creator=creator)
    return SQLDatabase(engine)

db = configure_db(db_uri)

## toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query = st.chat_input(placeholder="Ask anything from the database")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):

        try:
            # Run the query and handle the response
            response = agent.run(user_query)

            # Check for empty results
            if not response or "i don't know" in response.lower():
                response = "The query seems to be unrelated to the database, Please recheck."

        except Exception as e:
            # Handle invalid queries or errors in the execution
            response = f"An error occurred while processing your query: {str(e)}"

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
