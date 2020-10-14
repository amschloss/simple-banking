from datetime import date
from accounts import Account

class Service:
    """
    Parent class for Credit Card and Loan. Not intended to be instantiated on its own
    
    Attributes:
        owner (int): Customer number of the person who opened the service
        acct_number (int): Account number
        open_date (date): The date on which the service was opened
        balance (num): Balance on the service
        interest_rate (num): Interest rate on the account, in percent

    Methods:
        make_payment: Make a payment on the service
    """
    def __init__(self, owner, acct_number, balance, interest_rate, open_date = date.today()):
        self.owner = owner
        self._acct_number = acct_number
        self._balance = balance
        self._interest_rate = interest_rate
        self._open_date = open_date
    
    @property
    def acct_number(self):
        """Service account number"""
        return self._acct_number

    @property
    def balance(self):
        """Balance on the service"""
        return self._balance
    
    @property
    def interest_rate(self):
        """Interest rate on the account, in percent"""
        return self._interest_rate
    
    @property
    def open_date(self):
        """The date on which the service was opened"""
        return self._open_date
    
    def make_payment(self, amount, account: Account):
        """
        Makes a payment on the service.

        Args:
            amount(num): the payment amount
            account(Account): the source account for the payment funds

        Returns:
            the service balance after the withdrawal
        
        Raises:
            ValueError: insufficient balance in the account
        """
        if amount < account.balance:
            raise ValueError("Insufficient funds in account for this payment")
        account.withdraw(amount)
        self._balance -= amount
        return self._balance