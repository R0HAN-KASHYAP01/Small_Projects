import mysql.connector
from getpass import getpass
from tabulate import tabulate


class DatabaseHandler:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="#Coding",
            database="BankManagement"
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
   


class Account:
    def __init__(self, db_handler):
        self.db = db_handler
    
    def validate_account_number(self, account_number):
        query = "SELECT * FROM Accounts WHERE AccountNumber = %s"
        result = self.db.fetch_all(query, (account_number,))
        if result:
            return True
        else:
            False

    def create_account(self, name, account_type, initial_deposit, password):
        query = '''
        INSERT INTO Accounts (Name, AccountType, Balance, Password) VALUES (%s, %s, %s, %s)
        '''
        self.db.execute_query(query, (name, account_type, initial_deposit, password))
        print("Account created successfully!")

    def display_balance(self, account_number):
        query = "SELECT Balance FROM Accounts WHERE AccountNumber = %s"
        result = self.db.fetch_all(query, (account_number,))
        if result:
            return result[0][0]
        else:
            print("Account not found!")
            return None

    def deposit(self, account_number, new_balance):
        query = "UPDATE Accounts SET Balance = %s WHERE AccountNumber = %s"
        self.db.execute_query(query, (new_balance, account_number))
        

    def withdraw(self, account_number, new_balance, password):
        query = "SELECT Password FROM Accounts WHERE AccountNumber = %s"
        result = self.db.fetch_all(query, (account_number,))
        
        if not result:
            print("Account not found!")
            return

        stored_password = result[0][0]
        if password == stored_password:
            query = "UPDATE Accounts SET Balance = %s WHERE AccountNumber = %s"
            self.db.execute_query(query, (new_balance, account_number))

        else:
            print("Password is incorrect!")
    
    def Transaction_money(self,sender_acc,reciver_acc,password,money):
        if self.validate_account_number(sender_acc) and self.validate_account_number(reciver_acc):
            sender_balance = self.display_balance(sender_acc)
            if sender_balance >= money:
                sender_new_balance = sender_balance - money
                self.withdraw(sender_acc,sender_new_balance,password)
                reciver_balance = self.display_balance(reciver_acc)

                reciver_new_balance = reciver_balance + money
                self.deposit(reciver_acc,reciver_new_balance)
                
            else:
                print("Insufficent Balance!!")

        else:
            print("One or both account number may be wrong!!")


# Transaction Management
class Transaction:
    def __init__(self, db_handler):
        self.db = db_handler

    def record_transaction(self, account_number, trans_type, amount):
        query = '''
        INSERT INTO Transactions (AccountNumber, TransactionType, Amount)
        VALUES (%s, %s, %s)
        '''
        self.db.execute_query(query, (account_number, trans_type, amount))
        print("Transaction recorded.")
    
    def whole_record(self, account_number):
        query = '''
        SELECT * FROM Transactions WHERE AccountNumber = %s
        '''
        result = self.db.fetch_all(query, (account_number,))
        if result:
            # Define column headers based on the table structure
            headers = ["Transaction ID", "Account Number", "Transaction Type", "Amount"]
            print(tabulate(result, headers=headers, tablefmt="plain"))
        else:
            print("No transactions found for this account!")

# Main Bank System
class BankSystem:
    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.db_handler.connect()
        self.account_manager = Account(self.db_handler)
        self.transaction_manager = Transaction(self.db_handler)

    def display_menu(self):
        print("""
        1. Create Account
        2. Deposit
        3. Withdraw
        4. Display Balance
        5. Transaction Record
        6. Money Transfer
        7. Exit
    
        """)

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            if choice == '1':
                name = input("Enter name: ")
                acc_type = input("Enter account type (savings/current): ")
                initial_deposit = float(input("Enter initial deposit: "))
                password = getpass("Set a password: ")
                self.account_manager.create_account(name, acc_type, initial_deposit, password)

            elif choice == '2':
                acc_num = int(input("Enter account number: "))
                balance = self.account_manager.display_balance(acc_num)
                if balance is not None:
                    deposit_money = int(input("Enter deposit amount: "))
                    new_balance = balance + deposit_money
                    self.account_manager.deposit(acc_num, new_balance)
                    self.transaction_manager.record_transaction(acc_num, "deposit", deposit_money)
                    print("Deposit successful!!")
                    
                    

            elif choice == '3':
                acc_num = int(input("Enter account number: "))
                balance = self.account_manager.display_balance(acc_num)
                if balance is not None:
                    print(f"Current Balance: {balance}")
                    withdraw_amount = int(input("Enter withdrawal amount: "))
                    if withdraw_amount > balance:
                        print("Insufficient balance!")
                    else:
                        new_balance = balance - withdraw_amount
                        password = getpass("Enter your password: ")
                        self.account_manager.withdraw(acc_num, new_balance, password)
                        self.transaction_manager.record_transaction(acc_num, "withdraw", withdraw_amount)
                        print("Withdrawal successful!")
                        

            elif choice == '4':
                acc_num = int(input("Enter account number: "))
                balance = self.account_manager.display_balance(acc_num)
                if balance is not None:
                    print(f"Account Balance: {balance}")
            elif choice == '5':
                    acc_num = int(input("Enter account number: "))
                    self.transaction_manager.whole_record(acc_num)

            elif choice == "6":
                sender_acc = int(input("Enter the sender account Number: "))
                reciver_acc = int(input("Enter the reciver account Number: "))
                transfer_money = int(input("Enter the money to be transfer: "))
                password = getpass("Enter the password: ")
                self.account_manager.Transaction_money(sender_acc,reciver_acc,password,transfer_money)
                print("Transaction successful!!")
            elif choice == '7':
                print("Exiting...")
                self.db_handler.close_connection()
                break

            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    system = BankSystem()
    system.run()
