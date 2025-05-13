import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime
import os

# ATM Class with Persistent Data
class ATM:
    def __init__(self):
        self.balance = 0.0
        self.pin = None
        self.account_number = None
        self.transaction_history = []
        self.load_account()

    def load_account(self):
        """Load saved account details if available"""
        if os.path.exists("account.txt"):
            with open("account.txt", "r") as file:
                data = file.read().splitlines()
                if len(data) >= 3:
                    self.account_number = data[0]
                    self.pin = data[1]
                    self.balance = float(data[2])
                    self.transaction_history = data[3:]

    def save_account(self):
        """Save account details persistently"""
        with open("account.txt", "w") as file:
            file.write(f"{self.account_number}\n{self.pin}\n{self.balance}\n")
            file.write("\n".join(self.transaction_history))

    def validate_pin(self, entered_pin):
        return self.pin == entered_pin

    def register_account(self, pin, account_number):
        self.pin = pin
        self.account_number = account_number
        self.balance = 0.0
        self.transaction_history = []
        self.add_transaction("Account created with ₹0 balance")
        self.save_account()

    def deposit(self, amount):
        self.balance += amount
        self.add_transaction(f"Deposited ₹{amount}")
        self.save_account()
        return self.balance

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.add_transaction(f"Withdrew ₹{amount}")
            self.save_account()
            return self.balance
        else:
            raise ValueError("Insufficient funds")

    def check_balance(self):
        return self.balance

    def add_transaction(self, transaction):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_history.append(f"{timestamp} - {transaction}")
        self.save_account()

    def get_transaction_history(self):
        return self.transaction_history

# GUI Class
class ATM_GUI:
    def __init__(self, root, atm):
        self.root = root
        self.root.title("ATM Machine")
        self.atm = atm
        self.create_login_screen()

    def clear_screen(self):
        """Removes all widgets from the screen"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_login_screen(self):
        self.clear_screen()
        self.screen_title = tk.Label(self.root, text="ATM Login", font=("Arial", 24))
        self.screen_title.pack(pady=20)

        self.pin_label = tk.Label(self.root, text="Enter PIN:", font=("Arial", 14))
        self.pin_label.pack()
        self.pin_entry = tk.Entry(self.root, show="*", font=("Arial", 14))
        self.pin_entry.pack(pady=10)

        self.login_button = tk.Button(self.root, text="Login", font=("Arial", 14), command=self.login)
        self.login_button.pack(pady=10)

        if self.atm.pin is None:
            self.register_button = tk.Button(self.root, text="Register", font=("Arial", 14), command=self.create_registration_screen)
            self.register_button.pack(pady=10)

    def login(self):
        entered_pin = self.pin_entry.get()
        if self.atm.validate_pin(entered_pin):
            self.create_main_menu()
        else:
            messagebox.showerror("Error", "Invalid PIN. Try again.")

    def create_main_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="Main Menu", font=("Arial", 24)).pack(pady=20)

        tk.Button(self.root, text="Deposit", font=("Arial", 14), command=self.create_deposit_screen).pack(pady=10)
        tk.Button(self.root, text="Withdraw", font=("Arial", 14), command=self.create_withdraw_screen).pack(pady=10)
        tk.Button(self.root, text="Check Balance", font=("Arial", 14), command=self.show_balance).pack(pady=10)
        tk.Button(self.root, text="Transaction History", font=("Arial", 14), command=self.show_transaction_history).pack(pady=10)
        tk.Button(self.root, text="Exit", font=("Arial", 14), command=self.root.quit).pack(pady=10)

    def create_registration_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Register", font=("Arial", 24)).pack(pady=20)

        tk.Label(self.root, text="Enter Account Number:", font=("Arial", 14)).pack()
        account_entry = tk.Entry(self.root, font=("Arial", 14))
        account_entry.pack(pady=5)

        tk.Label(self.root, text="Set PIN:", font=("Arial", 14)).pack()
        pin_entry = tk.Entry(self.root, show="*", font=("Arial", 14))
        pin_entry.pack(pady=5)

        def register():
            account_number = account_entry.get()
            pin = pin_entry.get()
            if account_number and pin:
                self.atm.register_account(pin, account_number)
                messagebox.showinfo("Success", "Account registered successfully!")
                self.create_login_screen()
            else:
                messagebox.showerror("Error", "All fields are required.")

        tk.Button(self.root, text="Register", font=("Arial", 14), command=register).pack(pady=10)

    def create_deposit_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Deposit", font=("Arial", 24)).pack(pady=20)

        tk.Label(self.root, text="Enter Amount:", font=("Arial", 14)).pack()
        amount_entry = tk.Entry(self.root, font=("Arial", 14))
        amount_entry.pack(pady=10)

        def deposit():
            try:
                amount = float(amount_entry.get())
                new_balance = self.atm.deposit(amount)
                self.save_receipt(f"Deposited ₹{amount}")
                messagebox.showinfo("Success", f"Deposited ₹{amount}\nNew Balance: ₹{new_balance}")
                self.create_main_menu()
            except ValueError:
                messagebox.showerror("Error", "Invalid amount")

        tk.Button(self.root, text="Deposit", font=("Arial", 14), command=deposit).pack(pady=10)

    def create_withdraw_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Withdraw", font=("Arial", 24)).pack(pady=20)

        tk.Label(self.root, text="Enter Amount:", font=("Arial", 14)).pack()
        amount_entry = tk.Entry(self.root, font=("Arial", 14))
        amount_entry.pack(pady=10)

        def withdraw():
            try:
                amount = float(amount_entry.get())
                new_balance = self.atm.withdraw(amount)
                self.save_receipt(f"Withdrew ₹{amount}")
                messagebox.showinfo("Success", f"Withdrew ₹{amount}\nNew Balance: ₹{new_balance}")
                self.create_main_menu()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.root, text="Withdraw", font=("Arial", 14), command=withdraw).pack(pady=10)

    def show_balance(self):
        messagebox.showinfo("Balance", f"Your balance is: ₹{self.atm.check_balance()}")

    def show_transaction_history(self):
        history = "\n".join(self.atm.get_transaction_history())
        messagebox.showinfo("Transaction History", history if history else "No transactions found.")

    def save_receipt(self, transaction_detail):
        receipt_content = (
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Account: {self.atm.account_number}\n"
            f"{transaction_detail}\n"
            f"Balance: ₹{self.atm.check_balance()}\n"
        )

        with open("receipt.txt", "w") as file:
            file.write(receipt_content)

        messagebox.showinfo("Receipt", "Receipt saved as receipt.txt")

root = tk.Tk()
atm = ATM()
ATM_GUI(root, atm)
root.mainloop()
