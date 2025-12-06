from DataBase.DataBase import Database
from user_management.user import User
from user_management.payment_details import Payment
from user_management.request import Request
from exceptions import *
import bcrypt

class BankService:
    def __init__(self, db: Database):
        self.db = db

    def transfer_money(self, sender: str, receiver: str, amount: float):
        try:
            sender = self.db.get_user(sender)
            receiver = self.db.get_user(receiver)
        except AccountNotFoundError:
            raise AccountNotFoundError
        
        if amount <= 0:
            raise NegativeAmountError

        if (sender.balance < amount):
            raise InsufficientFundsError(f"Insuficient funds: {sender.balance}$ < {amount}$")
        
        sender.balance -= amount
        receiver.balance += amount

        # Create payment record
        payment = Payment(amount, sender.credentials.username, receiver.credentials.username)
        sender.payment_history.add_payment(payment)
        receiver.payment_history.add_payment(payment)

        self.db.modify_user(sender)
        self.db.modify_user(receiver)

    def transfer_iban(self, sender_user: User, iban: str, amount: float):
        """
        Transfers money to a user identified by IBAN.
        """
        if amount <= 0:
            raise NegativeAmountError

        if (sender_user.balance < amount):
            raise InsufficientFundsError(f"Insuficient funds: {sender_user.balance}$ < {amount}$")
        
        # Try to find the receiver by IBAN
        try:
            receiver_user = self.db.get_user_by_iban(iban)
        except AccountNotFoundError:
            raise AccountNotFoundError(f"No user found with IBAN: {iban}")

        sender_user.balance -= amount
        receiver_user.balance += amount
        
        # Create payment record
        payment = Payment(amount, sender_user.credentials.username, receiver_user.credentials.username)
        sender_user.payment_history.add_payment(payment)
        receiver_user.payment_history.add_payment(payment)
        
        self.db.modify_user(sender_user)
        self.db.modify_user(receiver_user)

    def refresh_user(self, user: User) -> User:
        user_updated = self.db.get_user(username=user.credentials.username)
        return user_updated

    def withdraw(self, user: User, amount: float):
        if (user.balance < amount):
            raise InsufficientFundsError(f"Insuficient funds: {user.balance}$ < {amount}$")
        
        user.balance -= amount
        self.db.modify_user(user)

    def add_money(self, user: User, amount: float, sender_name: str):
        user.balance += amount
        
        # Create payment record for the deposit
        payment = Payment(amount, sender_name, user.credentials.username)
        user.payment_history.add_payment(payment)
        
        self.db.modify_user(user)
    
    def checkUserLogin(self, username, Password):
        if self.db.checkUserLogin(username, Password):
            return True
        else:
            return False
        
    def is_card_unique(self, card_number):
        """
        Check if the card number is unique in the database.
        """
        if self.db.card_exists(card_number) == True:
            return False
        return True
    
    def is_username_unique(self, username):
        """
        Checks if the username is unique.
        """
        try:
            self.db.get_user(username)
            return False
        except AccountNotFoundError:
            return True
    
    def add_user(self, user : User):
        """
        Adds a new user to database.
        """
        self.db.add_user(user)

    def get_user(self, username):
        """
        Retrieves a user from the database.
        """
        return self.db.get_user(username)

    def delete_user(self, username):
        """
        Deletes a user from the database.
        """
        self.db.delete_user(username)

    def listen_to_user_changes(self, username, callback):
        """
        Listen to real-time changes for a user.
        """
        return self.db.listen_to_user(username, callback)

    def create_support_request(self, user: User, title: str, concern: str):
        """
        Creates and saves a support request for the user.
        """
        request = Request(
            username=user.credentials.username,
            email=user.credentials.email,
            title=title,
            concern=concern
        )
        self.db.add_request(request)


    