from sqlalchemy import Table, Column, Integer, String, MetaData, DATE
from sqlalchemy import create_engine, Sequence, ForeignKey, Float
from sqlalchemy.sql import select, and_
from bankpersons import Employee, Customer
from accounts import Account
from services import CreditCard, Loan

engine = create_engine("sqlite:///bankdata.sqlite")
metadata = MetaData()

# define tables
employees = Table('employees', metadata,
    Column('empid', Integer, Sequence('empid_seq'), primary_key = True),
    Column('firstname', String), Column('lastname', String),
    Column('address', String), Column('city', String),
    Column('state', String(2)), Column('zipcode', String(5)),
    Column('email', String)
)

customers = Table('customers', metadata,
    Column('custid', Integer, Sequence('custid_seq'), primary_key = True),
    Column('firstname', String), Column('lastname', String),
    Column('address', String), Column('city', String),
    Column('state', String(2)), Column('zipcode', String(5)),
    Column('email', String)
)

accounts = Table('accounts', metadata,
    Column('acctnum', Integer, primary_key = True),
    Column('owner', None, ForeignKey('customers.custid')),
    Column('accttype', String), Column('balance', Float),
    Column('intrate', Float)
)

credit_cards = Table('creditcards', metadata,
    Column('acctnum', Integer, primary_key = True),
    Column('owner', None, ForeignKey('customers.custid')),
    Column('balance', Float), Column('intrate', Float),
    Column('opendate', DATE), Column('limit', Float),
    Column('cashlimit', Float), Column('minpayment', Float)
)

loans = Table('loans', metadata,
    Column('acctnum', Integer, primary_key = True),
    Column('owner', None, ForeignKey('customers.custid')),
    Column('balance', Float), Column('intrate', Float),
    Column('opendate', DATE), Column('maturitydate', DATE),
    Column('monthlypmt', Float)
)

metadata.create_all(engine)
conn = engine.connect()

def employee_upsert(emp:Employee):
    """
    Adds a new or updates an existing Employee to the database.

    Arguments:
        emp(Employee): The employee to add/update
    """
    stmt = None
    is_new_emp = False
    if employee_srch(emp_id = emp.employee_number):
        stmt = employees.update().where(employees.c.empid == emp.employee_number)
    else:
        stmt = employees.insert()
        is_new_emp = True
    stmt = stmt.values(firstname=emp.first_name, lastname=emp.last_name, address=emp.address,
                       city=emp.city, state=emp.state, zipcode=emp.zipcode, email=emp.email)
    result = conn.execute(stmt)
    if is_new_emp:
        emp.employee_number = result.inserted_primary_key

def employee_srch(emp_id = None, first_name = None, last_name = None):
    """
    Finds Employees in the database.
    Searches by ID/employee number or full name; if no arguments are specified, searches for all employees

    Arguments (all optional):
        emp_id (int): An employee ID to search for
        first_name (str): An employee first name to search for
        last_name (str): An employee last name to search for

    Returns:
        a list of Employees meeting any criteria specified

    Raises:
        ValueError: only one of first_name and last_name are specified
    """
    stmt = select(employees)
    if emp_id == None and first_name == None and last_name == None:
        pass
    elif emp_id != None:
        stmt = stmt.where(employees.c.empid == emp_id)
    elif first_name != None and last_name != None:
        stmt = stmt.where(and_(employees.c.firstname == first_name, employees.c.lastname == last_name))
    else:
        raise ValueError("Please specify one of the following: no arguments, an employee ID, or both first AND last name")
    result = conn.execute(stmt)
    return [Employee(row['firstname'], row['lastname'], row['empid']).add_contact(
        row['address'], row['city'], row['state'], row['zipcode'], row['email']
    ) for row in result]

def customer_upsert(cust:Customer):
    """
    Adds a new or updates an existing Customer to the database.

    Arguments:
        cust(Customer): The customer to add/update
    """
    stmt = None
    is_new_cust = False
    if customer_srch(cust_id= cust.cust_number):
        stmt = customers.update().where(customers.c.custid == cust.cust_number)
    else:
        stmt = customers.insert()
        is_new_cust = True
    stmt = stmt.values(firstname=cust.first_name, lastname=cust.last_name, address=cust.address,
                       city=cust.city, state=cust.state, zipcode=cust.zipcode, email=cust.email)
    result = conn.execute(stmt)
    if is_new_cust:
        cust.cust_number = result.inserted_primary_key

def customer_srch(cust_id = None, first_name = None, last_name = None):
    """
    Finds Customers in the database.
    Searches by ID/customer number or full name; if no arguments are specified, searches for all customers

    Arguments (all optional):
        cust_id (int): A customer ID to search for
        first_name (str): A customer first name to search for
        last_name (str): A customer last name to search for

    Returns:
        a list of Customers meeting any criteria specified

    Raises:
        ValueError: only one of first_name and last_name are specified
    """
    stmt = select(customers)
    if cust_id == None and first_name == None and last_name == None:
        pass
    elif cust_id != None:
        stmt = stmt.where(customers.c.empid == cust_id)
    elif first_name != None and last_name != None:
        stmt = stmt.where(and_(customers.c.firstname == first_name, customers.c.lastname == last_name))
    else:
        raise ValueError("Please specify one of the following: no arguments, a customer ID, or both first AND last name")
    result = conn.execute(stmt)
    return [Customer(row['firstname'], row['lastname'], row['custid']).add_contact(
        row['address'], row['city'], row['state'], row['zipcode'], row['email']
    ) for row in result]

def account_upsert(acct:Account):
    """
    Adds a new or updates an existing Account to the database.

    Arguments:
        acct(Account): The account to add/update
    """
    stmt = None
    if account_srch(acct_num = acct.acct_number):
        stmt = accounts.update().where(accounts.c.acctnum == acct.acct_number)
    else:
        stmt = employees.insert()
    stmt = stmt.values(acctnum = acct.acct_number, owner = acct.owner, accttype = acct.type,
                       balance = acct.balance, intrate = acct.interest_rate)
    result = conn.execute(stmt)
    
def account_srch(acct_num = None, cust_num = None):
    """
    Finds Accounts in the database.
    Searches by account number, or customer number

    Arguments (one must be specified):
        acct_num (int): An account number to search for
        cust_num (int): A customer number to retrieve all accounts for

    Returns:
        a list of Accounts meeting any criteria specified

    Raises:
        ValueError: neither acct_num or cust_num are specified
    """
    stmt = select(accounts)
    if acct_num != None:
        stmt = stmt.where(accounts.c.acctnum == acct_num)
    elif cust_num != None:
        stmt = stmt.where(accounts.c.owner == cust_num)
    else:
        raise ValueError("Must specify either acct_num or cust_num to search for accounts")
    result = conn.execute(stmt)
    return [Account(row['owner'], row['acctnum'], row['accttype'], row['intrate']).deposit(row['balance']) for row in result]
