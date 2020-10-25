from accounts import Account
import services as sv

class Person:
    def __init__(self, first_name, last_name):
        """ 
        Create a Person with first and last name
        """
        self.first_name = first_name
        self.last_name = last_name
    
    def add_contact(self, address, city, state, zipcode, email):
        """
        Add contact information to a Person
        """
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.email = email

class Employee(Person):
    def __init__(self, first_name, last_name, employee_number):
        """
        Create an Employee with first and last name, and employee number
        """
        super().__init__(first_name, last_name)
        self.employee_number = employee_number
    
    def __repr__(self):
        return f'Employee ID {self.employee_number}: {self.first_name} {self.last_name}'

class Customer(Person):
    def __init__(self, first_name, last_name, cust_number):
        """
        Create a Customer with first and last name, and customer number
        Also initializes with empty lists of Accounts and Services
        """
        super().__init__(first_name, last_name)
        self.cust_number = cust_number
        self.services = []
        self.accounts = []
    
    def __repr__(self):
        return f'Customer ID {self.cust_number}: {self.first_name} {self.last_name}'

    def open_account(self, new_acct:Account):
        """Attach an account to the customer"""
        self.accounts.append(new_acct)

    def open_creditcard(self, new_card:sv.CreditCard):
        """Attach a credit card to the customer"""
        self.services.append(new_card)

    def open_loan(self, new_loan:sv.Loan):
        """Attach a loan to the customer"""
        self.services.append(new_loan)
        