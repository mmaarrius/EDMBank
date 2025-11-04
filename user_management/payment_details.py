from datetime import datetime

class Payment:
    """
    Contains the details of a transaction.
    """
    def __init__(self, amount: float, sender: str, receiver: str):
        self.amount = amount
        self.sender = sender
        self.receiver = receiver
        self.date = datetime.now()

class PaymentsHistory:
    """
    Represents all the payments made by the user.
    """
    def __init__(self):
        self.history: list[Payment] = []

    def add_payment(self, payment: Payment):
        self.history.append(payment)

