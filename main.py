import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt


# Connect to MySQL
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="244466666",
    database="student_performance"
)

cursor = connection.cursor()


# ---------------- ADD STUDENT ----------------
def add_student():

    print("\n----- Add Student -----")

    name = input("Enter student name: ")

    try:
        python_marks = int(input("Enter Python marks: "))
        dbms_marks = int(input("Enter DBMS marks: "))
        maths_marks = int(input("Enter Maths marks: "))

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

        print("\nStudent added successfully!")
        print("Name:", name)
        print("Total:", total)
        print("Percentage:", round(percentage, 2))
        print("Grade:", grade)

    except ValueError:
        print("\nPlease enter marks using numbers only!")


# ---------------- VIEW STUDENTS ----------------
def view_students():

    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()

    print("\n----- All Student Records -----")

    if len(records) == 0:
        print("No student records found.")

    else:
        for record in records:
            print(record)
# ---------------- SEARCH STUDENT ----------------
def search_student():

    name = input("\nEnter student name to search: ")

    query = "SELECT * FROM students WHERE name = %s"
    cursor.execute(query, (name,))

    record = cursor.fetchone()

    if record:
        print("\n----- Student Found -----")
        print("ID:", record[0])
        print("Name:", record[1])
        print("Python:", record[2])
        print("DBMS:", record[3])
        print("Maths:", record[4])
        print("Total:", record[5])
        print("Percentage:", record[6])
        print("Grade:", record[7])

    else:
        print("\nStudent not found!")

    # ---------------- UPDATE STUDENT ----------------


def update_student():
    try:
        student_id = int(input("\nEnter student ID to update: "))

        python_marks = int(input("Enter new Python marks: "))
        dbms_marks = int(input("Enter new DBMS marks: "))
        maths_marks = int(input("Enter new Maths marks: "))

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

        query = """
         UPDATE students
         SET python_marks = %s,
             dbms_marks = %s,
             maths_marks = %s,
             total = %s,
             percentage = %s,
             grade = %s
         WHERE id = %s
         """

        values = (
            python_marks,
            dbms_marks,
            maths_marks,
            total,
            percentage,
            grade,
            student_id
        )

        cursor.execute(query, values)
        connection.commit()

        if cursor.rowcount > 0:
            print("\nStudent record updated successfully!")
        else:
            print("\nStudent ID not found!")

    except ValueError:
        print("\nPlease enter numbers only!")

# ---------------- DELETE STUDENT ----------------
def delete_student():

    try:
        student_id = int(input("\nEnter student ID to delete: "))

        query = "DELETE FROM students WHERE id = %s"

        cursor.execute(query, (student_id,))
        connection.commit()

        if cursor.rowcount > 0:
            print("\nStudent record deleted successfully!")
        else:
            print("\nStudent ID not found!")

    except ValueError:
        print("\nPlease enter a valid student ID!")

# ---------------- STATISTICS ----------------
def statistics():

    query = "SELECT * FROM students"

    df = pd.read_sql(query, connection)

    if df.empty:
        print("\nNo student data available.")
        return

    print("\n----- Student Statistics -----")

    print("Average Python:", round(df["python_marks"].mean(), 2))
    print("Average DBMS:", round(df["dbms_marks"].mean(), 2))
    print("Average Maths:", round(df["maths_marks"].mean(), 2))

    print("Highest Percentage:", round(df["percentage"].max(), 2))
    print("Lowest Percentage:", round(df["percentage"].min(), 2))

# ---------------- GRAPH ----------------
def show_graph():

    query = "SELECT * FROM students"

    df = pd.read_sql(query, connection)

    if df.empty:
        print("\nNo student data available.")
        return

    plt.bar(df["name"], df["percentage"])

    plt.xlabel("Student Name")
    plt.ylabel("Percentage")
    plt.title("Student Performance")

    plt.show()
# ---------------- MAIN MENU ----------------
while True:

    print("\n===================================")
    print("     STUDENT PERFORMANCE ANALYZER")
    print("===================================")

    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Statistics")
    print("7. Graph")
    print("8. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        search_student()

    elif choice == "4":
        update_student()

    elif choice == "5":
        delete_student()

    elif choice == "6":
        statistics()

    elif choice == "7":
        show_graph()

    elif choice == "8":
        print("\nThank you for using Student Performance Analyzer!")
        break
    else:
        print("\nInvalid choice! Please enter 1, 2 or 3.")


# Close connection
cursor.close()
connection.close()