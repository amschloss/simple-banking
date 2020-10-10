class Account:
    """
    A class to represent a bank Account.

    Attributes
    ----------
    owner: int
        Customer number of the person who owns the account
    acct_number: int
        Account number
    type: str
        Account type - either 'savings' or 'checking'
    balance: num
        Balance in the account. Not allowed to go negative
    interest_rate: num
        Interest rate on the account. Cannot be zero for a savings account
    """
    def __init__(self, owner, acct_number, acct_type, interest_rate = 0):
        """
        Create a new Account of the specified type and interest rate
        """
        if acct_type.lower() not in ["savings", "checking"]:
            raise ValueError(f"{acct_type} is not a valid account type")
        if acct_type.lower() == 'savings' and interest_rate == 0:
            raise ValueError("Savings accounts must have an interest rate")
        self.owner = owner
        self.acct_number = acct_number
        self.type = acct_type.lower()
        self.balance = 0
        self.interest_rate = interest_rate

    def deposit(self, amount):
        """
        Make a deposit into this account.

        Parameter:
            amount(int): the amount to deposit
        """
        self.balance += amount
    