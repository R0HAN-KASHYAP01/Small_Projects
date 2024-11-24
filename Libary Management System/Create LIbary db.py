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
    # Creating the Database
    cursor.execute("Create database Libary")

    cursor.execute("Use Libary")


    # Creating the Table for the student record
    cursor.execute('''
        CREATE TABLE record (
            Rollno int(2) primary key,
            Name varchar(20),
            Class varchar(5),
            Book_name varchar(20),
            Due_date Date
        )
    ''')

    # Creating the Table for the Libary_book
    cursor.execute('''
            CREATE table Libary_book(
                    Book_Name varchar(30),
                    class varchar(20),
                    No_of_book integer
            )''')

    cursor.execute('Insert into Libary_book values ("Mathematics", "XII", 6)')
    cursor.execute('Insert into Libary_book values ("English", "XII",5)')
    cursor.execute('Insert into Libary_book values ("Physics", "XII",1)')
    cursor.execute('Insert into Libary_book values ("Chemistry", "XII",4)')
    cursor.execute('Insert into Libary_book values ("Computer Science", "XII",7)')

    cursor.execute('Insert into Libary_book values ("Mathematics", "XI", 6)')
    cursor.execute('Insert into Libary_book values ("English", "XI",5)')
    cursor.execute('Insert into Libary_book values ("Physics", "XI",3)')
    cursor.execute('Insert into Libary_book values ("Chemistry", "XI",4)')
    cursor.execute('Insert into Libary_book values ("Computer Science", "XI",7)')

    cursor.execute('Insert into Libary_book values ("Mathematics", "X", 6)')
    cursor.execute('Insert into Libary_book values ("English", "X",5)')
    cursor.execute('Insert into Libary_book values ("Physics", "X",3)')
    cursor.execute('Insert into Libary_book values ("Chemistry", "X",4)')
    cursor.execute('Insert into Libary_book values ("Computer Science", "X",7)')



    connection.commit()
    
except mysql.connector.Error as error:
        print(f"Error: {error}")
