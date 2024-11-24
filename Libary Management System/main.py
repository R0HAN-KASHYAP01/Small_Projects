
import mysql.connector


def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='#Shooting',
            database='Libary'
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


def no_of_book_available(book_name, Class, show_output=True):
    try:
        cursor.execute(
            "SELECT No_of_book FROM libary_book WHERE Book_name = %s AND class = %s", (book_name, Class))
        no_book = cursor.fetchone()
        if no_book:
            if show_output:
                print(
                    f"The no of books named {book_name} of class {Class} is available in libary are :- ")
            return no_book[0]
        else:
            print("No Data found!")
    except mysql.connector.Error as error:
        print(f"Error: {error}")


def Add_book(book_name, Class, no_of_book):
    try:
        cursor.execute(
            "SELECT * FROM libary_book WHERE Book_Name = %s AND Class = %s", (book_name, Class))
        result = cursor.fetchone()
        if result:
            print(
                f"The book '{book_name}' of class '{Class}' is already present in the library.")
        else:
            cursor.execute('''INSERT INTO libary_book (Book_Name,class,No_of_book)
                VALUES (%s,%s,%s)''', (book_name, Class, no_of_book))
            connection.commit()
            print("Book added successfully!")

    except mysql.connector.Error as error:
        print(f"Error: {error}")


def Lend_book(rollno, name, Class, book_name, Due_date):
    try:
        cursor.execute(
            "SELECT * FROM record WHERE Rollno = %s AND Name = %s AND Class = %s", (rollno, name, Class))
        result = cursor.fetchone()
        if result:
            print("You already take a book from the libary. Return that first!")
        else:
            no_of_books = no_of_book_available(
                book_name, Class, show_output=False)
            new_no_of_books = no_of_books - 1
            if no_of_books != 0:
                cursor.execute('''INSERT INTO record (Rollno,Name,Class,Book_name,Due_date)
                    VALUES (%s,%s,%s,%s,%s)''', (rollno, name, Class, book_name, Due_date))
                connection.commit()

                cursor.execute("UPDATE libary_book SET No_of_book = %s WHERE Book_name = %s AND class = %s", (
                    new_no_of_books, book_name, Class))
                connection.commit()
                print("Book Lended Successfully!")
            else:
                print(
                    f"Sorry All book of named {book_name} of Class {Class} is lended by other student!")

    except mysql.connector.Error as error:
        print(f"Error: {error}")


def remove_book(book_name, Class):
    try:
        cursor.execute("SELECT Book_Name, Class FROM libary_book ")
        result = cursor.fetchall()
        if (book_name, Class) in result:
            cursor.execute(
                "DELETE FROM libary_book WHERE Book_name = %s AND class = %s", (book_name, Class))
            connection.commit()
            print("Book remove successfully!")
        else:
            print(
                f"The book named {book_name} of Class {Class} not present in the libary!")
    except mysql.connector.Error as error:
        print(f"Error: {error}")


def return_book(rollno, name, Class, book_name):
    try:
        cursor.execute(
            "SELECT * FROM record WHERE Rollno = %s AND Name = %s AND Class = %s", (rollno, name, Class))
        result = cursor.fetchone()
        if result:
            cursor.execute(
                "DELETE FROM record WHERE Rollno = %s AND Name = %s", (rollno, name))
            connection.commit()
            print("Book returned Successfully!")

            no_of_books = no_of_book_available(
                book_name, Class, show_output=False)
            new_no_of_books = no_of_books + 1
            cursor.execute("UPDATE libary_book SET No_of_book = %s WHERE Book_name = %s AND class = %s",
                           (new_no_of_books, book_name, Class))
            connection.commit()
        else:
            print("You are already returned the book!")
    except mysql.connector.Error as error:
        print(f"Error: {error}")


def Display_book(Class):
    try:
        cursor.execute(
            "SELECT Book_Name, No_of_book FROM libary_book WHERE Class = %s", (Class,))
        books = cursor.fetchall()

        if books:
            print("Books available in Class:", Class)
            print("-" * 40)

            for book in books:
                print(f"Book Name: {book[0]}")
                print(f"Number of Books Available: {book[1]}")
                print("-" * 40)
        else:
            print("No Data found.")
    except mysql.connector.Error as error:
        print(f"Error: {error}")


while (True):

    print('''
Choose any of the option.
1. Number of books available in libary of the specific book
2. Add book in the libary
3. Lend book from the libary
4. Remove book from the libary
5. Return book in the libary
6. Display All the book of specific Class
        ''')

    user_choice = int(input())
    if user_choice == 1:
        book_name = input(
            "Enter the name of the book you want the deltail:-\n")
        Class = input(
            "Enter the class of which book you wanted the detail:-\n")
        result = no_of_book_available(book_name, Class)
        print(result)

    elif user_choice == 2:
        book_name = input("Enter the name of the book you want to add:-\n")
        Class = input("Enter the class of which book you wanted to add:-\n")
        no_of_book = int(input(
            f"How many of books named {book_name} of Class {Class} you want to add:-\n"))
        Add_book(book_name, Class, no_of_book)

    elif user_choice == 3:
        rollno = int(input("Enter the Roll no. :-\n"))
        name = input("Enter you name:-\n")
        Class = input("Enter the class of which book you wanted to lend:-\n")
        book_name = input("Enter the name of the book you want to lend:-\n")
        due_date = input(
            "Enter the date till you wanted the book in the format 'YYYY-MM-DD':-\n")
        Lend_book(rollno, name, Class, book_name, due_date)

    elif user_choice == 4:
        book_name = input("Enter the name of the book you want to remove:-\n")
        Class = input("Enter the class of which book you wanted to remove:-\n")
        remove_book(book_name, Class)

    elif user_choice == 5:
        rollno = int(input("Enter the Roll no. :-\n"))
        name = input("Enter you name:-\n")
        book_name = input("Enter the name of the book you want to return:-\n")
        Class = input("Enter the class of which book you wanted to return:-\n")
        return_book(rollno, name, Class, book_name)

    elif user_choice == 6:
        Class = input("Enter the class of which book you want to see:-\n")
        Display_book(Class)

    print("Enter the q for quit and c for continue: ")
    user_choice2 = " "
    while (user_choice2 != "q" and user_choice2 != "c"):
        user_choice2 = input()
        if user_choice2 == "q":
            print("Thank You!")
            exit()
        elif user_choice2 == "c":
            continue
