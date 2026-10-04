import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="YOUR_MYSQL_PASSWORD",
    database="student_performance"
)

query = "SELECT * FROM students"

df = pd.read_sql(query, connection)

plt.bar(df["name"], df["percentage"])

plt.xlabel("Student Name")
plt.ylabel("Percentage")

plt.title("Student Performance")

plt.xticks(rotation=30)

plt.tight_layout()

plt.show()

connection.close()