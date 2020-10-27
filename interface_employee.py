from datalayer import *

def set_up_employee(first_name, last_name):
    """
    Interactively builds an employee record.

    Arguments:
        first_name(str): the employee's first name
        last_name(str): the employee's last name

    Returns:
        a new Employee with the information input by the user
    """
    addr = input("What is your street address? ")
    city = input("What city do you live in? ")
    state = input("What state do you live in (2-letter postal abbreviation please)? ")
    zipcode = input("What is your zipcode (5 numbers only please)? ")
    email = input("And finally, what is your email? ")
    new_emp = Employee(first_name, last_name, 999)
    new_emp.add_contact(addr, city, state, zipcode, email)
    return new_emp
    
fname = input("What is your first name? ")
lname = input("What is your last name? ")
emp = employee_srch(first_name=fname, last_name=lname)
if not emp:
    print("I didn't find you, let's set you up.")
    emp = set_up_employee(fname, lname)
    employee_upsert(emp)
    print(f"Thanks {fname}! You're all set up, your employee number is {emp.employee_number}")
else:
    print(f"Welcome back, {fname}!")

