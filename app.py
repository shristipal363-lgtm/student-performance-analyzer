from flask import Flask, render_template, request, redirect
import mysql.connector
import matplotlib.pyplot as plt

app = Flask(__name__)


# MySQL connection
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="244466666",
    database="student_performance"
)

cursor = connection.cursor()


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Add Student page
@app.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        python_marks = int(request.form["python_marks"])
        dbms_marks = int(request.form["dbms_marks"])
        maths_marks = int(request.form["maths_marks"])

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

        return redirect("/")

    return render_template("add_student.html")


# View Students
@app.route("/students")
def view_students():

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    return render_template("students.html", students=students)

# ---------------- SEARCH STUDENT ----------------

@app.route("/search", methods=["GET", "POST"])
def search_student():

    student = None

    if request.method == "POST":

        name = request.form["name"]

        query = "SELECT * FROM students WHERE name = %s"

        cursor.execute(query, (name,))

        student = cursor.fetchone()

    return render_template("search.html", student=student)
# ---------------- UPDATE STUDENT ----------------

@app.route("/update", methods=["GET", "POST"])
def update_student():

    if request.method == "POST":

        student_id = int(request.form["id"])

        python_marks = int(request.form["python_marks"])
        dbms_marks = int(request.form["dbms_marks"])
        maths_marks = int(request.form["maths_marks"])

        # Calculate total
        total = python_marks + dbms_marks + maths_marks

        # Calculate percentage
        percentage = total / 3

        # Calculate grade
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

        # Update MySQL record
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

        return redirect("/students")

    return render_template("update_student.html")
# ---------------- STATISTICS ----------------

@app.route("/statistics")
def statistics():

    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()

    if len(records) == 0:
        return render_template("statistics.html",
                               average_python=0,
                               average_dbms=0,
                               average_maths=0,
                               highest_percentage=0,
                               lowest_percentage=0)

    python_marks = [row[2] for row in records]
    dbms_marks = [row[3] for row in records]
    maths_marks = [row[4] for row in records]
    percentages = [float(row[6]) for row in records]

    average_python = sum(python_marks) / len(python_marks)
    average_dbms = sum(dbms_marks) / len(dbms_marks)
    average_maths = sum(maths_marks) / len(maths_marks)

    highest_percentage = max(percentages)
    lowest_percentage = min(percentages)

    return render_template(
        "statistics.html",
        average_python=round(average_python, 2),
        average_dbms=round(average_dbms, 2),
        average_maths=round(average_maths, 2),
        highest_percentage=highest_percentage,
        lowest_percentage=lowest_percentage
    )

# ---------------- GRAPH ----------------

@app.route("/graph")
def graph():

    cursor.execute("SELECT name, percentage FROM students")
    records = cursor.fetchall()

    names = []
    percentages = []

    for record in records:
        names.append(record[0])
        percentages.append(float(record[1]))

    plt.figure(figsize=(8, 5))

    plt.bar(names, percentages)

    plt.xlabel("Student Name")
    plt.ylabel("Percentage")
    plt.title("Student Performance")

    plt.xticks(rotation=30)

    plt.tight_layout()

    plt.savefig("static/graphs/student_performance.png")

    plt.close()

    return render_template("graph.html")


if __name__ == "__main__":
    app.run(debug=True)


if __name__ == "__main__":
    app.run(debug=True)