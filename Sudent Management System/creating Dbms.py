
import mysql.connector


def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='#Shooting',
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


try:
    # Creating Database:-
    cursor.execute("Create Database CLass_12")

    cursor.execute("Use Class_12")

    cursor.execute('''Create Table Students(
    Rollno integer PRIMARY KEY,
    Name varchar(20),
    DOB date,
    Father_name varchar(20),
    Mother_name varchar(20),
    contact_number BIGINT,
    Course varchar(10),
    Present_days integer,
    Absent_days integer,
    Percentage_Attendence integer
    )''')

    cursor.execute('''INSERT INTO Students (Rollno, Name, DOB, Father_name, Mother_name, contact_number, Course, Present_days, Absent_days)
    VALUES
    (1, 'Rohan', '2006-01-15', 'XYZ', 'XZY', 8178019905, 'PCM', 90, 10),
    (2, 'Atul', '2006-10-23', 'ABC', 'CBA', 8755365623, 'PCM', 88, 12),
    (3, 'Uday', '2006-07-17', 'UVW', 'WVU', 9520507815, 'PCM', 95, 5);
    ''')

    cursor.execute('''
    UPDATE Students
    SET Percentage_Attendence = (Present_days / (Present_days + Absent_days)) * 100
    ''')

    connection.commit()

except mysql.connector.Error as error:
    print(f"Error: {error}")
