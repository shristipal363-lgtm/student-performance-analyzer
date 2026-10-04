import mysql.connector

# Connect to MySQL
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="244466666",
    database="student_performance"
)

cursor = connection.cursor()
print("\n----- All Student Records -----")

cursor.execute("SELECT * FROM students")

records = cursor.fetchall()

for record in records:
    print(record)

# Student details
name = input("Enter student name: ")
python_marks = int(input("Enter Python marks: "))
dbms_marks = int(input("Enter DBMS marks: "))
maths_marks = int(input("Enter Maths marks: "))

# Calculate result
total = python_marks + dbms_marks + maths_marks
percentage = total / 3

if percentage >= 90:
    grade = "A+"
elif percentage >= 80:
    grade = "A"
elif percentage >= 70:
    grade = "B"
elif percentage >= 60:
    grade = "C"
elif percentage >= 40:
    grade = "D"
else:
    grade = "F"

# Insert into database
query = """
INSERT INTO students
(name, python_marks, dbms_marks, maths_marks, total, percentage, grade)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

values = (
    name,
    python_marks,
    dbms_marks,
    maths_marks,
    total,
    percentage,
    grade
)

cursor.execute(query, values)
connection.commit()

print("\nStudent record saved successfully!")
print("Name:", name)
print("Total:", total)
print("Percentage:", round(percentage, 2))
print("Grade:", grade)

cursor.close()
connection.close()