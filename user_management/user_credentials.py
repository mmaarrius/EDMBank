MIN_PASS_LEN = 5

class UserCredentials:
    """
    Represents user's credentials for registration.
    Can also be used for login.
    """
    
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    
    @staticmethod
    def check_password(password: str) -> bool:
        """
        Checks the password of a user for registration.
        """
        if len(password) < MIN_PASS_LEN:
            return False
        return True
    

    # TODO [when the database is ready]
    @staticmethod
    def check_username(username: str) -> bool:
        """Check if the username is valid/available in the database."""
        return True

    @staticmethod
    def check_email(email: str) -> bool:
        """
        Checks if the email is valid.
        """
        if "@" in email and "." in email:
            return True
        else:
            return False

    

        