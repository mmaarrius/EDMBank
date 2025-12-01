import random
from datetime import datetime

class Card :
    def __init__(self, number, cvv, expiry_date, IBAN):
        self.number = number
        self.cvv = cvv
        self.expiry_date = expiry_date
        self.IBAN = IBAN

    
    @staticmethod
    def generateCard():
        """
        Generates a random card for the user.
        It must be validated externally to ensure the card does not already exist in the database.
        """
        # Card number (16 digits)
        number = random.randrange(10**15, 10**16)

        # CVV (3 digits)
        cvv = random.randrange(100, 1000)

        # Expiry date
        current_year = datetime.now().year
        rand_year = random.randrange(current_year + 1, current_year + 20)
        rand_month = random.randrange(1, 13)

        expiry_date = f"{rand_month:02d}/{rand_year % 100:02d}"

        # IBAN
        iban_number = str(random.randrange(10**29, 10**30))
        IBAN = "IBANEDM" + iban_number

        return Card(number, cvv, expiry_date, IBAN)

    