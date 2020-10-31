class Account:
    """
    A class to represent a bank Account. Accounts all initialize with zero balance.

    Attributes:
        owner (int): Customer number of the person who owns the account
        acct_number (int): Account number
        type (str): Account type - either 'savings' or 'checking'
        balance (num): Balance in the account
        interest_rate (num): Interest rate on the account, in percent. Cannot be zero for a savings account

    Methods:
        deposit: Add an amount to the balance
        withdraw: Deduct an amount from the balance. Balance cannot go negative
        pay_interest: Apply interest to the balance
    """
    def __init__(self, owner, acct_number, acct_type, interest_rate = 0):
        """
        Creates a new Account of the specified type and interest rate.

        Args:
            owner (int): Customer number of the person who owns the account
            acct_number (int): Account number
            acct_type (str): Account type - either 'savings' or 'checking'
            interest_rate (num): Interest rate on the account, in percent
        
        Raises:
            ValueError: acct_type is neither 'savings' nor 'checking', or interest rate is 0 and type is 'savings'
        """
        if acct_type.lower() not in ["savings", "checking"]:
            raise ValueError(f"{acct_type} is not a valid account type")
        if acct_type.lower() == 'savings' and interest_rate == 0:
            raise ValueError("Savings accounts must have an interest rate")
        self.owner = owner
        self.acct_number = acct_number
        self._type = acct_type.lower()
        self._balance = 0
        self._interest_rate = interest_rate

    def __repr__(self):
        base_repr = f'{self.type} account nbr {self.acct_number} has balance ${round(self.balance, 2)}'
        if self.interest_rate != 0:
            base_repr += f' at {round(self.interest_rate, 2)}% interest'
        return base_repr

    @property
    def balance(self):
        """Balance in this account"""
        return self._balance

    @property
    def interest_rate(self):
        """Annual interest rate on the account, in percent"""
        return self._interest_rate
    
    @property
    def type(self):
        """Account type, checking or savings"""
        return self._type
    
    def deposit(self, amount):
        """
        Makes a deposit into this account.

        Args:
            amount(num): the amount to deposit

        Returns:
            the account balance after the deposit

        Raises:
            ValueError: attempted to deposit negative amount
        """
        if amount < 0:
            raise ValueError("Negative deposit not allowed")
        self._balance += amount
        return self._balance

    def withdraw(self, amount):
        """
        Makes a withdrawal from this account.

        Args:
            amount(num): the amount to withdraw

        Returns:
            the account balance after the withdrawal
        
        Raises:
            ValueError: balance would be negative, or attempted to withdraw negative amount
        """
        if amount > self._balance:
            raise ValueError("Insufficient funds to make this withdrawal")
        if amount < 0:
            raise ValueError("Negative withdrawal not allowed")
        self._balance -= amount
        return self._balance

    def pay_interest(self):
        """
        Applies monthly interest to the account. The rate is the annual rate / 12

        Returns:
            the account balance after applying interest
        """
        multiplier = 1 + self._interest_rate / 1200.0
        self._balance *= multiplier
        return self._balance
        