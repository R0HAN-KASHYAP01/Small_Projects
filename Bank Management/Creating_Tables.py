import mysql.connector
from mysql.connector import errorcode

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='#Coding'
        )
        print("Database connected successfully.")
        return connection

    except mysql.connector.Error as error:
        print(f"Error connecting to database: {error}")
        return None


try:
    connection = connect_to_database()
    if not connection:
        raise Exception("Failed to connect to the database.")

    cursor = connection.cursor()

    # Create the database if it doesn't exist
    cursor.execute("SHOW DATABASES")
    if ('BankManagement',) not in cursor.fetchall():
        cursor.execute("CREATE DATABASE BankManagement")
        print("Database 'BankManagement' created.")

    cursor.execute("USE BankManagement")

    # Create Accounts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Accounts(
        AccountNumber INT PRIMARY KEY AUTO_INCREMENT,
        Name VARCHAR(100),
        AccountType VARCHAR(20),
        Balance DECIMAL(15, 2),
        Password VARCHAR(100)
    )
    ''')
    print("Table 'Accounts' created or already exists.")

    # Create Transactions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Transactions (
        TransactionID INT PRIMARY KEY AUTO_INCREMENT,
        AccountNumber INT,
        TransactionType VARCHAR(20),
        Amount DECIMAL(15, 2),
        DateTime DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (AccountNumber) REFERENCES Accounts(AccountNumber)
    )
    ''')
    print("Table 'Transactions' created or already exists.")

    connection.commit()
    print("All changes committed successfully.")

except mysql.connector.Error as error:
    print(f"Database error: {error}")

finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'connection' in locals() and connection:
        connection.close()
    print("Database connection closed.")
