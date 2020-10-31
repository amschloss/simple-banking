# Customer interface for the simple banking system
# Allows the customer to:
#   Set themselves up as a customer, if need be
#   Review their accounts/services
#   Open a new account/service
#   Make a payment

from datalayer import *
from random import randint, random
import logging

def set_up_customer(first_name, last_name):
    """
    Interactively builds a customer record.

    Arguments:
        first_name(str): the customer's first name
        last_name(str): the customer's last name

    Returns:
        a new Customer with the information input by the user
    """
    addr = input("What is your street address? ")
    city = input("What city do you live in? ")
    state = input("What state do you live in (2-letter postal abbreviation please)? ")
    zipcode = input("What is your zipcode (5 numbers only please)? ")
    email = input("And finally, what is your email? ")
    new_cust = Customer(first_name, last_name, 999)
    new_cust.add_contact(addr, city, state, zipcode, email)
    logging.info(f"Created new {new_cust}")
    return new_cust

def load_accts(cust:Customer):
    """Loads all accounts and services for the specified Customer."""
    cust.accounts = account_srch(cust_num=cust.cust_number)
    cust.services = credit_card_srch(cust_num=cust.cust_number)
    loans = loan_srch(cust_num=cust.cust_number)
    if len(loans) > 0:
        cust.services.append(loans)

def view_accts(cust:Customer):
    """Prints all of the specified Customer's accounts and services."""
    header = f"Accounts for {cust.first_name} {cust.last_name}:"
    header_deco = '=' * len(header)
    print(header_deco)
    print(header)
    print(header_deco)
    if len(cust.accounts) == 0:
        print("No checking or savings accounts on file")
    else:
        for acct in cust.accounts:
            print(acct)
    print(header_deco)
    if len(cust.services) == 0:
        print("No credit cards or loans on file")
    else:
        for svc in cust.services:
            print(svc)
    print(header_deco)

def new_acct(cust:Customer):
    """Interactively opens a new Account for the specified Customer."""
    print("Which type of account are you opening today?")
    response_type = ''
    while response_type not in ('c', 's'):
        print("C. Checking")
        print("S. Savings")
        response_type = input(">> ").lower()
        if response_type not in ('c', 's'):
            print("Please type either C for Checking or S for Savings.")
    acct_types = {'c': "Checking", 's': "Savings"}
    starting_bal = float(input("How much would you like to deposit to open this account? >> "))
    acct_num = randint(1000000000, 9999999999)
    int_rate = 0
    if response_type == 's':
        int_rate = random() * 3
    new_account = Account(cust.cust_number, acct_num, acct_types[response_type], int_rate)
    new_account.deposit(starting_bal)
    cust.open_account(new_account)
    account_upsert(new_account)
    logging.info(f"{cust} opened new {new_account}")
    print("Account opened successfully:", new_account)

def make_deposit(cust:Customer):
    """Interactively allow the Customer to make a deposit to one of their accounts."""
    accts_enum = list(enumerate(cust.accounts))
    print("Which account?")
    for idx,acct in accts_enum:
        print(f"{idx}. {acct}")
    try:
        choice = int(input(">> "))
        dep_amt = float(input("How much to deposit? >> "))
        acct = accts_enum[choice][1]
        new_bal = acct.deposit(dep_amt)
    except ValueError as err:
        print(err)
        print("Deposit canceled. Please enter positive numbers.")
    else:
        account_upsert(acct)
        logging.info(f"{cust} deposited ${round(dep_amt, 2)} into account {acct.acct_number}; new balance ${round(new_bal, 2)}")
        print("Deposit successful!")

def make_withdrawal(cust:Customer):
    pass

def new_card(cust:Customer):
    cred_limit = randint(10, 50) * 100
    acct_num = randint(1000000000, 9999999999)
    int_rate = random() * 10 + 15
    card = CreditCard(cust.cust_number, acct_num, int_rate, cred_limit)
    cust.open_creditcard(card)
    credit_card_upsert(card)
    logging.info(f"{cust} opened new {card}")
    print("Credit card opened successfully:", card)

def card_charge(cust:Customer):
    pass

def new_loan(cust:Customer):
    pass

def make_pmt(cust:Customer):
    pass

logging.basicConfig(filename="transaction.log", level=logging.INFO, 
                    format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
fname = input("What is your first name? ")
lname = input("What is your last name? ")
cust = customer_srch(first_name=fname, last_name=lname)
if not cust:
    print("I didn't find you, let's set you up.")
    cust = set_up_customer(fname, lname)
    customer_upsert(cust)
    print(f"Thanks {fname}! You're all set up, your customer number is {cust.cust_number}")
else:
    load_accts(cust)
    print(f"Welcome back, {fname}!")

selection = 1
choices = {1: view_accts, 2: new_acct, 3: make_deposit, 4: make_withdrawal, 5: new_card, 
           6: card_charge, 7: new_loan, 8: make_pmt, 0: lambda x: ""}
while selection != 0:
    print("What would you like to do?")
    print("1. See my existing accounts and services")
    print("2. Open a new account")
    print("3. Make a deposit")
    print("4. Make a withdrawal")
    print("5. Open a new credit card")
    print("6. Make a charge against a card")
    print("7. Open a new loan")
    print("8. Make a card/loan payment")
    print("0. Exit")
    selection = int(input(">> "))
    action = choices.get(selection, lambda x: print("Sorry, that isn't one of the choices, please try again."))
    action(cust)
print("Pleasure doing business with you. Goodbye!")
