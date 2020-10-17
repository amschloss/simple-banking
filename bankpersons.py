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

class Customer(Person):
    def __init__(self, first_name, last_name, cust_number):
        """
        Create a Customer with first and last name, and customer number
        Also initializes with empty lists of Accounts and Services
        """
        super().__init__(first_name, last_name)
        self._cust_number = cust_number
        self.services = []
        self.accounts = []
    
    @property
    def cust_number(self):
        """Customer number"""
        return self._cust_number

    def open_account(self, acct_num, acct_type, init_bal, interest_rate):
        """
        Open an account of the specified type
        """
        new_acct = Account(self.cust_number, acct_num, acct_type, interest_rate)
        new_acct.deposit(init_bal)
        self.accounts.append(new_acct)

    def open_creditcard(self, new_card:sv.CreditCard):
        self.services.append(new_card)

    def open_loan(self, new_loan:sv.Loan):
        self.services.append(new_loan)
        