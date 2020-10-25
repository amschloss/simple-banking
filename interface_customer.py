from datalayer import *

def one_line_input(prompt):
    """
    Prompts the user for input and collects it all on the same line.

    Arguments:
        prompt(str): the prompt to present to the user
    
    Returns:
        the user input in string format
    """
    print(prompt, end=' > ')
    response = input()
    return response

def set_up_customer(first_name, last_name):
    """
    Interactively builds a customer record.

    Arguments:
        first_name(str): the customer's first name
        last_name(str): the customer's last name

    Returns:
        a new Customer with the information input by the user
    """
    addr = one_line_input("What is your street address?")
    city = one_line_input("What city do you live in?")
    state = one_line_input("What state do you live in (2-letter postal abbreviation please)?")
    zipcode = one_line_input("What is your zipcode (5 numbers only please)?")
    email = one_line_input("And finally, what is your email?")
    new_cust = Customer(first_name, last_name, 999)
    new_cust.add_contact(addr, city, state, zipcode, email)
    return new_cust
    
fname = one_line_input("What is your first name?")
lname = one_line_input("What is your last name?")
cust = customer_srch(first_name=fname, last_name=lname)
if not cust:
    print("I didn't find you, let's set you up.")
    cust = set_up_customer(fname, lname)
    customer_upsert(cust)
    print(f"Thanks {fname}! You're all set up, your customer number is {cust.cust_number}")
else:
    print(f"Welcome back, {fname}!")

