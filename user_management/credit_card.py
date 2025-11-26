import random
from datetime import datetime

class Card :
    def __init__(self, number, cvv, expiry_date, IBAN):
        self.number = number
        self.cvv = cvv
        self.expiry_date = expiry_date
        self.IBAN = IBAN

    
    @staticmethod
    def generateCardNumber():
        """
        Generates a random card number for the user.
        It must be validated externally to ensure the card does not already exist in the database.
        """
        number = random.randrange(10**15,10**16-1)
        cvv = random.randrange(10**2,10**3)
        # Added expiry date
        current_year = datetime.now().year
        year_first = current_year + 1
        year_last = current_year + 20
        rand_year = random.randrange(year_first, year_last)
        IBAN = "IBANEDM" + random.randrange(10**29, 10**30-1)
        rand_month = random.randrange(1,12)
        if rand_month < 10:
            expiry_date = "0" + str(rand_month) + "/" + str(rand_year%100) 
        else:
            expiry_date = str(rand_month) + "/" + str(rand_year%100)
        return number, cvv, expiry_date, IBAN

    