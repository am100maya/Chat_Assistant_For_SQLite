import sqlite3

#Connect to SQLite Database
conn = sqlite3.connect("company.db")
cursor = conn.cursor()

#Create the departments table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        id INT,
        name TEXT PRIMARY KEY,
        manager TEXT NOT NULL
    )
""")

#Create the employees table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        salary REAL NOT NULL,
        hire_date TEXT NOT NULL,
        FOREIGN KEY (department) REFERENCES departments(name)
    )
""")

#Insert Sample Data
cursor.execute("INSERT OR IGNORE INTO departments (id, name, manager) VALUES (1, 'Sales', 'Alice')")
cursor.execute("INSERT OR IGNORE INTO departments (id, name, manager) VALUES (2, 'Engineering', 'Bob')")
cursor.execute("INSERT OR IGNORE INTO departments (id, name, manager) VALUES (3, 'Marketing', 'Charlie')")

cursor.execute("INSERT OR IGNORE INTO employees (id, name, department, salary, hire_date) VALUES (1, 'Alice', 'Sales', 50000, '2021-01-15')")
cursor.execute("INSERT OR IGNORE INTO employees (id, name, department, salary, hire_date) VALUES (2, 'Bob', 'Engineering', 70000, '2020-06-10')")
cursor.execute("INSERT OR IGNORE INTO employees (id, name, department, salary, hire_date) VALUES (3, 'Charlie', 'Marketing', 60000, '2022-03-20')")
cursor.execute("INSERT OR IGNORE INTO employees (id, name, department, salary, hire_date) VALUES (4, 'David', 'Engineering', 55000, '2021-03-20')")
#Commit changes and close connection
conn.commit()
conn.close()

print("Tables created and sample data added successfully!")
