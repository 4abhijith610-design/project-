"""
Student Management System (DBMS Project)
Database: SQLite3
"""

import sqlite3
import sys

DB_NAME = "student_mgmt.db"


# ==========================================
# DATABASE SETUP & INITIALIZATION
# ==========================================
def get_db_connection():
    """Returns a database connection with foreign keys enabled."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def initialize_database():
    """Creates required tables and inserts default admin user if missing."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Table 1: Users (Authentication & Authorization)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('Admin', 'Staff'))
        )
    """)

    # Table 2: Courses
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT UNIQUE NOT NULL,
            instructor TEXT NOT NULL
        )
    """)

    # Table 3: Students (Foreign Key linked to Courses)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses (course_id) ON DELETE CASCADE
        )
    """)

    # Seed Default Admin Account
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ('admin', 'admin123', 'Admin')
        )
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ('staff', 'staff123', 'Staff')
        )

    # Seed Sample Course Data
    cursor.execute("SELECT COUNT(*) FROM courses")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO courses (course_name, instructor) VALUES ('Computer Science', 'Dr. Smith')")
        cursor.execute("INSERT INTO courses (course_name, instructor) VALUES ('Mathematics', 'Prof. Johnson')")

    conn.commit()
    conn.close()


# ==========================================
# INPUT VALIDATION UTILITIES
# ==========================================
def get_non_empty_input(prompt):
    """Ensures user input is not blank or whitespace."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Error: Input cannot be empty. Please try again.")


def get_integer_input(prompt):
    """Ensures user input is a valid positive integer."""
    while True:
        try:
            value = int(input(prompt).strip())
            if value > 0:
                return value
            print("Error: Please enter a positive integer.")
        except ValueError:
            print("Error: Invalid number format. Please enter digits only.")


# ==========================================
# AUTHENTICATION MODULE
# ==========================================
def register_user():
    """Allows new users to register as Staff accounts."""
    print("\n--- USER REGISTRATION ---")
    username = get_non_empty_input("Enter new username: ")
    password = get_non_empty_input("Enter password: ")
    role = "Staff"  # Self-registration defaults to Staff role for security

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       (username, password, role))
        conn.commit()
        print(f"Success: User '{username}' registered as Staff!")
    except sqlite3.IntegrityError:
        print(f"Error: Username '{username}' already exists. Try another.")
    finally:
        conn.close()


def login():
    """Authenticates users and returns user dict on success."""
    print("\n--- USER LOGIN ---")
    username = get_non_empty_input("Username: ")
    password = get_non_empty_input("Password: ")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username, role FROM users WHERE username = ? AND password = ?", 
                   (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"\nLogin successful! Welcome {user[1]} ({user[2]})")
        return {"id": user[0], "username": user[1], "role": user[2]}
    else:
        print("Error: Invalid username or password.")
        return None


# ==========================================
# CRUD OPERATIONS (STUDENTS & COURSES)
# ==========================================
def view_all_courses():
    """Displays all available courses."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    rows = cursor.fetchall()
    conn.close()

    print("\n" + "="*45)
    print(f"{'ID':<5} | {'Course Name':<20} | {'Instructor':<15}")
    print("="*45)
    for r in rows:
        print(f"{r[0]:<5} | {r[1]:<20} | {r[2]:<15}")
    print("="*45)


def add_course():
    """Admin Only: Add a new course."""
    print("\n--- ADD NEW COURSE ---")
    name = get_non_empty_input("Course Name: ")
    instructor = get_non_empty_input("Instructor Name: ")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO courses (course_name, instructor) VALUES (?, ?)", (name, instructor))
        conn.commit()
        print("Success: Course added successfully!")
    except sqlite3.IntegrityError:
        print("Error: Course name already exists.")
    finally:
        conn.close()


def create_student():
    """Add a new student record linked to a course ID."""
    print("\n--- ADD NEW STUDENT ---")
    name = get_non_empty_input("Student Full Name: ")
    email = get_non_empty_input("Email: ")
    age = get_integer_input("Age: ")

    view_all_courses()
    course_id = get_integer_input("Select Course ID from above list: ")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO students (name, email, age, course_id) VALUES (?, ?, ?, ?)",
                       (name, email, age, course_id))
        conn.commit()
        print("Success: Student record created!")
    except sqlite3.IntegrityError as e:
        if "FOREIGN KEY" in str(e).upper():
            print("Error: Invalid Course ID selected.")
        else:
            print("Error: Email already exists.")
    finally:
        conn.close()


def view_students():
    """View students with JOIN query to get course name."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.student_id, s.name, s.email, s.age, c.course_name
        FROM students s
        JOIN courses c ON s.course_id = c.course_id
    """)
    rows = cursor.fetchall()
    conn.close()

    print("\n" + "="*70)
    print(f"{'ID':<5} | {'Name':<18} | {'Email':<22} | {'Age':<5} | {'Course':<15}")
    print("="*70)
    if not rows:
        print("No student records found.")
    else:
        for r in rows:
            print(f"{r[0]:<5} | {r[1]:<18} | {r[2]:<22} | {r[3]:<5} | {r[4]:<15}")
    print("="*70)


def update_student():
    """Update student information."""
    view_students()
    student_id = get_integer_input("\nEnter Student ID to update: ")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    student = cursor.fetchone()

    if not student:
        print("Error: Student ID not found.")
        conn.close()
        return

    print("Leave field blank to keep existing value.")
    new_name = input(f"New Name [{student[1]}]: ").strip() or student[1]
    new_email = input(f"New Email [{student[2]}]: ").strip() or student[2]
    
    new_age_str = input(f"New Age [{student[3]}]: ").strip()
    new_age = int(new_age_str) if new_age_str.isdigit() else student[3]

    view_all_courses()
    new_course_str = input(f"New Course ID [{student[4]}]: ").strip()
    new_course = int(new_course_str) if new_course_str.isdigit() else student[4]

    try:
        cursor.execute("""
            UPDATE students 
            SET name = ?, email = ?, age = ?, course_id = ?
            WHERE student_id = ?
        """, (new_name, new_email, new_age, new_course, student_id))
        conn.commit()
        print("Success: Student record updated successfully!")
    except sqlite3.IntegrityError:
        print("Error: Invalid Course ID or Duplicate Email.")
    finally:
        conn.close()


def delete_student():
    """Admin Only: Delete a student record."""
    view_students()
    student_id = get_integer_input("\nEnter Student ID to DELETE: ")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    if not cursor.fetchone():
        print("Error: Student ID not found.")
        conn.close()
        return

    confirm = input(f"Are you sure you want to delete student ID {student_id}? (yes/no): ").strip().lower()
    if confirm in ['yes', 'y']:
        cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        conn.commit()
        print("Success: Student record deleted.")
    else:
        print("Deletion canceled.")
    conn.close()


# ==========================================
# MENUS & INTERFACE
# ==========================================
def admin_menu(current_user):
    """Menu options reserved for Admin users."""
    while True:
        print(f"\n====================================")
        print(f"      ADMIN MENU ({current_user['username']})      ")
        print(f"====================================")
        print("1. View All Students")
        print("2. Add New Student")
        print("3. Update Student Record")
        print("4. Delete Student Record")
        print("5. View Courses")
        print("6. Add New Course")
        print("7. Logout")
        
        choice = input("Enter choice (1-7): ").strip()
        if choice == "1":
            view_students()
        elif choice == "2":
            create_student()
        elif choice == "3":
            update_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            view_all_courses()
        elif choice == "6":
            add_course()
        elif choice == "7":
            print("Logging out...")
            break
        else:
            print("Invalid selection! Please enter a number from 1 to 7.")


def staff_menu(current_user):
    """Menu options reserved for Staff users (Limited Permissions)."""
    while True:
        print(f"\n====================================")
        print(f"      STAFF MENU ({current_user['username']})      ")
        print(f"====================================")
        print("1. View All Students")
        print("2. Add New Student")
        print("3. Update Student Record")
        print("4. View Courses")
        print("5. Logout")
        
        choice = input("Enter choice (1-5): ").strip()
        if choice == "1":
            view_students()
        elif choice == "2":
            create_student()
        elif choice == "3":
            update_student()
        elif choice == "4":
            view_all_courses()
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid selection! Please enter a number from 1 to 5.")


def main():
    """Main application Loop."""
    initialize_database()

    while True:
        print("\n====================================")
        print("   STUDENT DBMS MAIN SYSTEM MENU   ")
        print("====================================")
        print("1. Login")
        print("2. Register New Staff Account")
        print("3. Exit System")

        choice = input("Select Option (1-3): ").strip()

        if choice == "1":
            user = login()
            if user:
                if user["role"] == "Admin":
                    admin_menu(user)
                elif user["role"] == "Staff":
                    staff_menu(user)
        elif choice == "2":
            register_user()
        elif choice == "3":
            print("\nExiting System. Goodbye!")
            sys.exit()
        else:
            print("Invalid option! Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()