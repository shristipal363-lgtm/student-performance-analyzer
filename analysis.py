import mysql.connector
import pandas as pd

# Connect to MySQL
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="244466666",
    database="student_performance"
)

# Read student data from MySQL
query = "SELECT * FROM students"

df = pd.read_sql(query, connection)

print("\n----- Student Data -----")
print(df)

print("\n----- Average Marks -----")
print("Python:", df["python_marks"].mean())
print("DBMS:", df["dbms_marks"].mean())
print("Maths:", df["maths_marks"].mean())

print("\n----- Highest Marks -----")
print("Python:", df["python_marks"].max())
print("DBMS:", df["dbms_marks"].max())
print("Maths:", df["maths_marks"].max())

connection.close()