class InsufficientFundsError(Exception):
    """Raised when an account doesn't have enough funds."""
    pass

class AccountNotFoundError(Exception):
    """Raised when an account doesn't exist."""
    pass
