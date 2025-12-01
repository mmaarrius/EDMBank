from DataBase.DataBase import Database
from user_management.user import User
from exceptions import *
import bcrypt

class BankService:
    def __init__(self, db: Database):
        self.db = db

    def transfer_money(self, sender: User, receiver: User, amount: float):
        if (sender.balance < amount):
            raise InsufficientFundsError(f"Insuficient funds: {sender.balance}$ < {amount}$")
        
        sender.balance -= amount
        receiver.balance += amount
        self.db.modify_user(sender)
        self.db.modify_user(receiver)

    def withdraw(self, user: User, amount: float):
        if (user.balance < amount):
            raise InsufficientFundsError(f"Insuficient funds: {user.balance}$ < {amount}$")
        
        user.balance -= amount
        self.db.modify_user(user)

    def add_money(self, user: User, amount: float):
        user.balance += amount
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
    