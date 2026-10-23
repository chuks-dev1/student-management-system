import sqlite3


def connect_database():
    """Connect to the student database."""
    connection = sqlite3.connect("students.db")
    return connection


def create_tables():
    """Create the students table if it doesn't exist."""
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL, age INTEGER NOT NULL, course TEXT NOT NULL, math_score REAL NOT NULL, 
      english_score REAL NOT NULL, science_score REAL NOT NULL)""")

    connection.commit()
    connection.close()


def add_student():
    """Add a new student to the database."""
    print("--- REGISTER A STUDENT ---")

    name = input("Enter a student name: ").strip()

    if not name:
        print("Please name cannot be empty.")
        return

    try:
        age = int(input("Enter student age: "))
        if age < 1 or age > 120:
            print("Please enter a valid age.")
            return

        course = input("Enter course: ").strip()
        if not course:
            print("Course cannot be empty.")
            return

        math_score = float(input('Enter mathematics score (0-100): '))
        english_score = float(input("Enter english score (1-100): "))
        science_score = float(input("Enter science score (1-100): "))

        scores = [math_score, english_score, science_score]

        if any(score < 0 or score > 100 for score in scores):
            print("Scores must be between 0 and 100.")
            return
    except ValueError:
        print("Invalid input. Please enter numbers where required.")
        return

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""INSERT INTO students (name, age, course, math_score, english_score, science_score)
          VALUES (?, ?, ?, ?, ?, ?)""", (name, age, course, math_score, english_score, science_score))

    connection.commit()
    connection.close()

    print(f"✅ Student '{name}' registered successfully!")


def view_students():
    """Display all student records."""
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    connection.close()

    if not students:
        print("\nno students registered yet.")
        return

    print("-------- ALL STUDENTS --------")

    for student in students:
        print(f"\nStudent ID: {student[0]}")
        print(f"Name: {student[1]}")
        print(f"Age: {student[2]}")
        print(f"Course: {student[3]}")
        print(f"Mathematics: {student[4]}")
        print(f"English: {student[5]}")
        print(f"Science: {student[6]}")
        print("-" * 35)


def search_student():
    """Search for students by ID or name."""
    print("\n---SEARCH FOR A STUDENT---")
    search_term = input("Enter student ID or name: ").strip()

    if not search_term:
        print("Please enter a student ID or name")
        return

    connection = connect_database()
    cursor = connection.cursor()

    if search_term.isdigit():
        cursor.execute("SELECT * FROM students WHERE id = ?",
                       (int(search_term),))
        students = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM students WHERE name LIKE ?",
                       (F"%{search_term}%", ))
        students = cursor.fetchall()
    connection.close()

    if not students:
        print("No matching student found.")
        return

    print("\n======== SEARCH RESULTS ========")

    for student in students:
        print(f"Student ID: {student[0]}")
        print(f"Name: {student[1]}")
        print(f"Age: {student[2]}")
        print(f"Course: {student[3]}")
        print(f"Mathematics: {student[4]}")
        print(f"English: {student[5]}")
        print(f"Science: {student[6]}")
        print("-" * 35)


def update_student():
    """Update an existing student's details."""
    print("\n--- UPDATE STUDENT DETAILS ---")

    try:
        student_id = int(input("Enter the student ID  to update: "))
    except ValueError:
        print("Please enter a valid student ID.")
        return

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()

    if student is None:
        connection.close()
        print("No student found with that ID.")
        return

    print(f"\nUpdating record for: {student[1]}")
    print("Press Enter to keep an existing value.")

    name_input = input(f"Name [{student[1]}]: ").strip()
    age_input = input(f"Age [{student[2]}]: ").strip()
    course_input = input(f"Course [{student[3]}]: ").strip()

    math_input = input(f"Mathematics [{student[4]}]: ").strip()
    english_input = input(f"English [{student[5]}]: ").strip()
    science_input = input(f"Science [{student[6]}]: ").strip()

    try:
        name = name_input if name_input else student[1]
        age = int(age_input) if age_input else student[2]
        course = course_input if course_input else student[3]

        math_score = float(math_input) if math_input else student[4]
        english_score = float(english_input) if english_input else student[5]
        science_score = float(science_input) if science_input else student[6]

        if not name:
            print("Name cannot be empty.")
            connection.close()
            return

        if age < 1 or age > 120:
            print("Age mustb be between 1 and 120.")
            connection.close()
            return

        if not course:
            print("Course cannot be empty.")
            connection.close()
            return

        scores = [math_score, english_score, science_score]

        if any(score < 0 or score > 100 for score in scores):
            print("Scores must be between 0 and 100.")
            connection.close()
            return

    except ValueError:
        print("Invalid input. Please check the age and scores.")
        connection.close()
        return

    cursor.execute("""UPDATE students 
    SET name = ?, age = ?, course = ?, math_score = ?, english_score = ?, science_score = ?
    WHERE id = ? """, (name, age, course, math_score, english_score, science_score, student_id))

    connection.commit()
    connection.close()

    print(f"Student ID {student_id} updated successfully.")


def delete_student():
    """Delete a student after confirmation."""
    print("\n--- DELETE STUDENT ---")

    try:
        student_id = int(input("Enter a student ID to delete."))
    except ValueError:
        print("Please enter a valid student ID.")
        return

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM students WHERE id  = ?", (student_id, ))
    student = cursor.fetchone()

    if student is None:
        connection.close()
        print("No student found with that ID.")
        return

    print(f"Student found: {student[0]}")

    confirmation = input(
        "Are you sure you want to delete this student? (yes/no): ").strip().lower()
    if confirmation != "yes":
        connection.close()
        print("Deletion cancelled.")
        return

    cursor.execute("DELETE FROM students WHERE id = ?", (student_id, ))

    connection.commit()
    connection.close()

    print(f"Student '{student[0]}' deleted successfully.")


def calculate_grade(average):
    """Determine a grade from a student's average """
    if average >= 70:
        return "A"
    elif average >= 60:
        return "B"
    elif average >= 50:
        return "C"
    elif average >= 45:
        return "D"
    elif average >= 40:
        return "E"
    else:
        return "F"


def student_report():
    """Display student averages, grades, and top performers."""
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    connection.close()

    if not students:
        print("\nNo student record available.")
        return

    print("\n====== STUDENT PERFORMANCE REPORT ======")

    top_students = []
    highest_average = -1

    for student in students:
        math_score = student[4]
        english_score = student[5]
        science_score = student[6]

        average = (math_score + english_score + science_score) / 3
        grade = calculate_grade(average)

        print(f"\nStudent: {student[1]}")
        print(f"Student ID: {student[0]}")
        print(f"Course: {student[3]}")
        print(f"Mathematics: {math_score:.2f}")
        print(f"English: {english_score:.2f}")
        print(f"Science: {science_score:.2f}")
        print(f"Average: {average:.2f}")
        print(f"Grade: {grade}")
        print("-" * 35)

        if average > highest_average:
            highest_average = average
            top_students = [student[1]]

        elif average == highest_average:
            top_students.append(student[1])

    print("\nTop-performing student(s):")
    for name in top_students:
        print(name)
    print(f"Highest average: {highest_average:.2f}")


def main():
    create_tables()

    while True:
        print("\n🎓 Student Management System")
        print("1. Add a student.")
        print("2. View all students.")
        print("3. Search for a student.")
        print("4. Update student details.")
        print("5. Delete a student.")
        print("6. View student reports.")
        print("7. Exit.")

        choice = input("Enter your choice (1-7): ")

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
            student_report()

        elif choice == "7":
            print("Goodbye!👋")
            break

        else:
            print("Invalid choice. Please enter a number fron 1 to 7.")


if __name__ == "__main__":
    main()
