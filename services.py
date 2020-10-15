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
        interest_rate (num): Annual interest rate on the account, in percent

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
        """Annual interest rate on the account, in percent"""
        return self._interest_rate
    
    @property
    def open_date(self):
        """The date on which the service was opened"""
        return self._open_date
    
    def make_payment(self, amount, account: Account):
        """
        Makes a payment on the service.

        Args:
            amount(num): the payment amount. If this amount is greater than the balance on the service, zeroes out the balance
            account(Account): the source account for the payment funds

        Returns:
            the service balance after the withdrawal
        
        Raises:
            ValueError: insufficient balance in the account
        """
        if amount < account.balance:
            raise ValueError("Insufficient funds in account for this payment")
        if amount > self.balance:
            amount = self.balance
        account.withdraw(amount)
        self._balance -= amount
        return self._balance

class CreditCard(Service):
    """
    Credit Card extends Service
    
    Attributes:
        owner (int): Customer number of the person who opened the card
        acct_number (int): Card number
        open_date (date): The date on which the card was opened
        balance (num): Balance on the card
        interest_rate (num): Annual interest rate on the card, in percent
        credit_limit (num): The maximum balance this card can have
        cash_advance_limit (num): The maximum amount of cash this card can advance to its owner
        minimum_payment (num): The minimum monthly payment that must be made on this card
        expiration_date (date): The date on which this card expires

    Methods:
        make_payment: Make a payment on the card (inherited)
        charge: Charge an amount to the card
        advance_cash: Pay out a cash advance against the card
    """

    def __init__(self, owner, acct_number, interest_rate, credit_limit, cash_advance_limit, open_date=date.today(), minimum_payment = 25, balance = 0):
        super().__init__(owner, acct_number, balance, interest_rate, open_date=open_date)
        self.credit_limit = credit_limit
        self.cash_advance_limit = cash_advance_limit
        self._minimum_payment = minimum_payment
        self.expiration_date = self.open_date.replace(self.open_date.year + 3)

    @property
    def minimum_payment(self):
        """
        The minimum monthly payment that must be made on this CreditCard.
        Either $25, or 10% of the current balance, whichever is greater
        """
        return max(self._minimum_payment, self.balance / 10)
    
    def charge(self, amount):
        """
        Charge an amount to this CreditCard

        Args:
            amount (num): the amount to charge
        
        Returns:
            the card balance after the charge

        Raises:
            ValueError: amount of charge would put the balance over the limit, decline transaction
        """
        if self.balance + amount > self.credit_limit:
            raise ValueError("Transaction declined, credit limit would be breached")
        self._balance += amount
        return self._balance

    def advance_cash(self, amount):
        """
        Pay out a cash advance against this CreditCard

        Args:
            amount (num): the amount to advance
        
        Returns:
            the card balance after the advance

        Raises:
            ValueError: amount of advance would put the balance over the limit, decline transaction
        """
        if self.balance + amount > self.cash_advance_limit:
            raise ValueError("Advance declined, cash advance limit would be breached")
        self._balance += amount
        return self._balance

    def charge_interest(self):
        """
        Applies interest to the CreditCard. The rate is the annual rate / 12

        Returns:
            the card balance after applying interest
        """
        multiplier = 1 + self._interest_rate / 1200.0
        self._balance *= multiplier
        return self._balance
        
class Loan(Service):
    """
    Loan extends Service
    
    Attributes:
        owner (int): Customer number of the person who opened the loan
        acct_number (int): Loan number
        open_date (date): The date on which the loan was opened
        balance (num): Balance on the loan
        interest_rate (num): Annual interest rate on the loan, in percent
        maturity_date(num): The date the loan matures

    Methods:
        make_payment: Make a payment on the loan (overridden)
        calculate_amortization: Determine the monthly payment
    """
