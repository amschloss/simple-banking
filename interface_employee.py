from datalayer import *
import logging

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

def view_accts():
    for cust in customers:
        header = f"Accounts for {cust.first_name} {cust.last_name}:"
        header_deco = '=' * len(header)
        print(header_deco)
        print(header)
        print(header_deco)
        if len(cust.accounts) == 0:
            print("No accounts on file")
        else:
            for acct in cust.accounts:
                print(acct)
            print(header_deco)
        if len(cust.services) == 0:
            print("No services on file")
        else:
            for svc in cust.services:
                print(svc)
    print('=' * 20)

def run_month_end():
    acct_ctr = 0
    svc_ctr = 0
    for cust in customers:
        for acct in cust.accounts:
            if acct.interest_rate > 0:
                new_bal = acct.pay_interest()
                account_upsert(acct)
                logging.info(f"Interest paid on account {acct.acct_number}, new balance ${round(new_bal, 2)}")
                acct_ctr += 1
        for svc in cust.services:
            if type(svc) == CreditCard:
                new_bal = svc.charge_interest()
                credit_card_upsert(svc)
                logging.info(f"Interest charged on card {svc.acct_number}, new balance ${round(new_bal, 2)}")
                svc_ctr += 1
    print(f"Month end process complete. {acct_ctr} accounts and {svc_ctr} credit cards affected. See transaction log for details.")

logging.basicConfig(filename="transaction.log", level=logging.INFO, 
                    format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
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

customers = customer_srch()
for cust in customers:
    load_accts(cust)
selection = 1
choices = {1: view_accts, 2: run_month_end, 0: lambda: ""}
while selection != 0:
    print("What would you like to do?")
    print("1. View all accounts")
    print("2. Apply interest to all accounts")
    print("0. Exit")
    selection = int(input(">> "))
    action = choices.get(selection, lambda: print("Sorry, that isn't one of the choices, please try again."))
    action()
print("Thank you. Goodbye")
