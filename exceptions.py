class InsufficientFundsError(Exception):
    """Raised when an account doesn't have enough funds."""
    pass

class AccountNotFoundError(Exception):
    """Raised when an account doesn't exist."""
    pass

class NegativeAmountError(Exception):
    """Raised when the transsfer amount is negative."""
    pass

class RequestError(Exception):
    """Raised when there is an error processing a support request."""
    pass