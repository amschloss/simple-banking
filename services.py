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
        """
        Creates a new Service.

        Attributes:
        owner (int): Customer number of the person who opened the service
        acct_number (int): Account number
        open_date (date): The date on which the service was opened
        balance (num): Balance on the service
        interest_rate (num): Annual interest rate on the account, in percent
        """
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
    
    @staticmethod
    def _advance_date(orig_date: date, num_years):
        """
        Advance a date by a number of years, to the first day of the following month
        
        Arguments:
            orig_date (date): the original date to be advanced
            num_years (int): the number of years to advance the date

        Returns:
            the advanced date
        """
        return orig_date.replace(year = orig_date.year + num_years, month = orig_date.month + 1, day = 1)

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

    def __init__(self, owner, acct_number, interest_rate, credit_limit, cash_advance_limit = 0, open_date=date.today(), minimum_payment = 25, balance = 0):
        """
        Opens a new credit card, that expires 3 years after opening.

        Attributes:
        owner (int): Customer number of the person who opened the card
        acct_number (int): Account number
        open_date (date): The date on which the card was opened
        balance (num): Balance on the card. Default is 0; if this is a balance transfer specify an initial balance
        interest_rate (num): Annual interest rate on the card, in percent
        credit_limit (num): The maximum balance this card can have
        cash_advance_limit (num): The maximum amount of cash this card can advance to its owner. If not specified, defaults to 25% of credit limit
        minimum_payment (num): The minimum monthly payment that must be made on this card
        """
        super().__init__(owner, acct_number, balance, interest_rate, open_date=open_date)
        self.credit_limit = credit_limit
        self.cash_advance_limit = cash_advance_limit if cash_advance_limit != 0 else self.credit_limit / 4
        self._minimum_payment = minimum_payment
        self._expiration_date = self._advance_date(open_date, 3)

    @property
    def minimum_payment(self):
        """
        The minimum monthly payment that must be made on this CreditCard.
        Either $25, or 10% of the current balance, whichever is greater
        """
        return max(self._minimum_payment, self.balance / 10)

    @property
    def expiration_date(self):
        """The date on which this card expires"""
        return self._expiration_date

    def __repr__(self):
        return f'Credit card nbr {self.acct_number} has balance ${self.balance} of ${self.credit_limit} at {self.interest_rate}%; minimum payment ${self.minimum_payment}'
    
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
    Loan extends Service. Assumes payments will be made monthly
    
    Attributes:
        owner (int): Customer number of the person who opened the loan
        acct_number (int): Loan number
        open_date (date): The date on which the loan was opened
        balance (num): Balance on the loan
        interest_rate (num): Annual interest rate on the loan, in percent
        maturity_date (date): The date the loan matures
        monthly_payment (num): The required monthly payment

    Methods:
        make_payment: Make a payment on the loan (overridden)
        calculate_amortization: (re)Calculate the monthly payment
    """

    def __init__(self, owner, acct_number, balance, interest_rate, open_date=date.today(), term=30, maturity_date = None, monthly_pmt = None):
        """
        Creates a new Loan.

        Attributes:
        owner (int): Customer number of the person who opened the loan
        acct_number (int): Loan account number
        open_date (date): The date on which the loan was opened. Defaults to today
        balance (num): Opening balance of the loan
        interest_rate (num): Annual interest rate on the loan, in percent
        term (num): Loan term, in years. Defaults to 30
        maturity_date (date): The date the loan matures. Defaults to calculate based on term
        monthly_pmt (num): The required monthly payment. Defaults to calculate based on term
        """
        super().__init__(owner, acct_number, balance, interest_rate, open_date=open_date)
        self._maturity_date = maturity_date if maturity_date is None else self._advance_date(open_date, term)
        self._monthly_pmt = monthly_pmt if monthly_pmt is None else self.calculate_amortization(term * 12)

    @property
    def maturity_date(self):
        return self._maturity_date

    @property
    def monthly_payment(self):
        return self._monthly_pmt

    def __repr__(self):
        return f'Loan nbr {self.acct_number} has balance ${self.balance} at {self.interest_rate}%, monthly payment ${self.monthly_payment}, matures on {self.maturity_date}'
    
    def calculate_amortization(self, num_pays: int):
        """
        Calculates the monthly payment on this loan.

        Arguments:
            num_pays (int): Number of payments to be made on the loan
        
        Returns:
            the monthly payment
        """
        r = self._interest_rate / 1200.0
        mp = self._balance * r / (1 - (1 + r) ** num_pays)
        return mp
