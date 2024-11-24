import mysql.connector


def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='#Shooting',
            database='Class_12'
        )
        return connection
    except mysql.connector.Error as error:
        print(f"Error: {error}")
        return None


try:
    connection = connect_to_database()
    if not connection:
        pass
    cursor = connection.cursor()
except mysql.connector.Error as error:
    print(f"Error: {error}")


def Fetch_Details(rollno):
    try:
        cursor.execute("SELECT * FROM Students WHERE Rollno = %s", (rollno,))

        student_data = cursor.fetchone()

        if student_data:
            rollno, name, dob, father_name, mother_name, contact_number, course, present_days, absent_days, percentage_attendance = student_data
            print(f"Roll No: {rollno}")
            print(f"Name: {name}")
            print(f"DOB: {dob}")
            print(f"Father's Name: {father_name}")
            print(f"Mother's Name: {mother_name}")
            print(f"Contact Number: {contact_number}")
            print(f"Course: {course}")
            print(f"Present Days: {present_days}")
            print(f"Absent Days: {absent_days}")
            print(f"Percentage Attendance: {percentage_attendance}%")
        else:
            print("No Data found.")

    except mysql.connector.Error as error:
        print(f"Error: {error}")


def Change_data(rollno):
    try:
        Fetch_Details(rollno)

        print("Which Data you want to change.")
        print("Rollno, Name, DOB, Father_name, Mother_name, contact_number, Course, Present_days, Absent_days")
        changing = input()
        new_data = input(f"Enter the new value of {changing}:-\n")

        cursor.execute("UPDATE Students SET {} = %s WHERE Rollno = %s".format(
            changing), (new_data, rollno))
        connection.commit()
        print("Your data changed successfully!")
    except mysql.connector.Error as error:
        print(f"Error: {error}")


def Details_of_specific_data(rollno):
    try:
        print("Which of these details do you want?")
        print("Rollno, Name, DOB, Father_name, Mother_name, contact_number, Course, Present_days, Absent_days")
        choice = input()
        cursor.execute(
            "SELECT {} FROM Students WHERE Rollno = %s".format(choice), (rollno,))
        detail = cursor.fetchone()

        if detail is not None:
            print(f"{choice}: {detail[0]}")
        else:
            print("No Data found.")

        connection.commit()
    except mysql.connector.Error as error:
        print(f"Error: {error}")


def New_Student(rollno, name, dob, father_name, mother_name, contact_number, course, present_day, absent_day):
    try:
        cursor.execute('''INSERT INTO Students (Rollno, Name, DOB, Father_name, Mother_name, contact_number, Course, Present_days, Absent_days)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                       (rollno, name, dob, father_name, mother_name, contact_number, course, present_day, absent_day))
        cursor.execute('''
                    UPDATE Students
                    SET Percentage_Attendence = (Present_days / (Present_days + Absent_days)) * 100
                        ''')
        connection.commit()
        print("New Student enter successfully!")
    except mysql.connector.Error as error:
        print(f"Error: {error}")


def Attendance():
    try:
        cursor.execute("SELECT COUNT(*) FROM Students")
        result = cursor.fetchone()
        print("Mark Attendance\n A => Absent\n P => Present")
        print("'Rollno', 'Name' :- P/A")
        print('-' * 40)

        for i in range(1, result[0] + 1):
            cursor.execute("SELECT Name FROM Students WHERE Rollno = %s", (i,))
            student = cursor.fetchone()
            while True:
                marking = input(f"{i}, {student[0]} :- ")
                if marking == "P":
                    cursor.execute(
                        "SELECT Present_days FROM Students WHERE Rollno = %s", (i,))
                    present = cursor.fetchone()
                    presents = present[0] + 1
                    cursor.execute(
                        "UPDATE Students SET Present_days = %s WHERE Rollno = %s", (presents, i))
                    connection.commit()
                    break
                elif marking == "A":
                    cursor.execute(
                        "SELECT Absent_days FROM Students WHERE Rollno = %s", (i,))
                    Absent = cursor.fetchone()
                    Absents = Absent[0] + 1
                    cursor.execute(
                        "UPDATE Students SET Absent_days = %s WHERE Rollno = %s", (Absents, i))
                    connection.commit()
                    break
                else:
                    print(
                        "Invalid input. Please enter 'P' for Present or 'A' for Absent.")

            cursor.execute('''
                        UPDATE Students
                        SET Percentage_Attendence = (Present_days / (Present_days + Absent_days)) * 100
                            ''')
            connection.commit()
        print('-' * 40)
        print("Attendane Done of all the student!")
    except mysql.connector.Error as error:
        print(f"Error: {error}")


def Delete_student(rollno):
    try:
        cursor.execute("DELETE FROM Students WHERE Rollno = %s", (rollno,))
        connection.commit()
        print(f"Student of Rollno {rollno} has been deleted.")

        cursor.execute("SELECT MAX(Rollno) FROM Students")
        max_rollno = cursor.fetchone()

        if max_rollno[0] >= rollno:
            for new_rollno in range(rollno, max_rollno[0]):
                cursor.execute(
                    "UPDATE Students SET Rollno = %s WHERE Rollno = %s", (new_rollno, new_rollno + 1))
                connection.commit()

    except mysql.connector.Error as error:
        print(f"Error: {error}")


def List_Student():
    try:
        cursor.execute("SELECT Rollno, Name FROM Students")
        students = cursor.fetchall()
        if students:
            print("The list of student in the class:- ")
            print("-" * 40)
            for student in students:
                print(f"Roll No: {student[0]}")
                print(f"Name: {student[1]}")
                print("-" * 40)
        else:
            print("No Data found.")

    except mysql.connector.Error as error:
        print(f"Error: {error}")


while (True):

    print('''
Choose any of the option.
1. Student Details
2. Update Student Detail
3. Details for a specific entry of student
4. Entry of new student
5. Attendance
6. Delete Student
7. List of Students in the class
          ''')

    user_choice = int(input())
    if user_choice == 1:
        rollno = int(input("Enter the Roll no. :-\n"))
        Fetch_Details(rollno)

    elif user_choice == 2:
        rollno = int(input("Enter the Roll no. :-\n"))
        Change_data(rollno)
    elif user_choice == 3:
        rollno = int(input("Enter the Roll no. :-\n"))
        Details_of_specific_data(rollno)
    elif user_choice == 4:
        rollno = int(input("Enter the Roll no. :-\n"))
        name = input("Enter the name of the student:-\n")
        dob = input("Enter the DOB of the student in YYYY-MM-DD format:-\n")
        father_name = input("Enter the Father's name of the student:-\n")
        mother_name = input("Enter the Mother's name of the student:-\n")
        contact = int(input("Enter the contact number of the student:-\n"))
        course = input("Enter the side/Course of the student:-\n")
        present = input("Enter the no of days student is present:-\n")
        absent = input("Enter the no of days student is absent:-\n")
        New_Student(rollno, name, dob, father_name, mother_name,
                    contact, course, present, absent)
    elif user_choice == 5:
        Attendance()
    elif user_choice == 6:
        rollno = int(input("Enter the Roll no. :-\n"))
        Delete_student(rollno)
    elif user_choice == 7:
        List_Student()

    print("Enter the q for quit and c for continue: ")
    user_choice2 = " "
    while (user_choice2 != "q" and user_choice2 != "c"):
        user_choice2 = input()
        if user_choice2 == "q":
            print("Thank You!")
            exit()
        elif user_choice2 == "c":
            continue
