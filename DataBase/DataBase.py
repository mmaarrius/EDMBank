import bcrypt
import os
import bcrypt
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from faker import Faker
from datetime import datetime
from user_management.user import User
from user_management.credit_card import Card
from user_management.user_credentials import UserCredentials
from user_management.payment_details import PaymentsHistory

class Database:
    def __init__(self):
        self.init_dadabase()

    def init_dadabase(self):
        key_path = os.path.join(os.path.dirname(__file__),"edmbank-7fd19-firebase-adminsdk-fbsvc-97c017e5cd.json")
        if not firebase_admin._apps:
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()


    def add_user(self, user : User):
        """Add a new user to the database."""
        password = user.credentials.password
        username = user.credentials.username
        CardDigit = user.card.number
        CVV = user.card.cvv
        email = user.credentials.email
        history = user.payment_history
    
        Password_bytes = str(Password).encode()
        salt = bcrypt.gensalt()
        Password = bcrypt.hashpw(Password_bytes, salt)
        Password = Password.decode()

        # TODO : all the necessary data is found in the User object (card, history, etc..).
        # Database should memorise all the fields
        # user_data = {
        #     "Name" : username,
        #     "Password_hash" : Password,
        #     "Card_Number" : CardDigit,
        #     "CVV" : CVV,
        #     "Expiry_date" : expiry_date,
        #     "Sold" : sum,
        #     "Email" : email,
        #     "Istoric" : []
        # }
        self.db.collection("Users").document(username).set(user_data)

    def checkUserLogin(self, username, Password):
        doc_ref = self.db.collection("Users").document(username)
        doc = doc_ref.get()

        if not doc.exists:
            return False
        stored_hash = doc.to_dict().get("Password_hash")
        if bcrypt.checkpw(Password.encode(), stored_hash.encode()):
            return True
        else:
            return False

    def getData(self, username, date):
        doc_ref = self.db.collection("Users").document(username)
        doc = doc_ref.get()
        
        if date == 1:
            return doc.get("Card_Number")
        elif date == 2:
            return doc.get("CVV")
        elif date == 3:
            return doc.get("Expiry_date")
        elif date == 4:
            return doc.get("Sold")
        elif date == 5:
            return doc.get("Email")
        elif date == 6:
            return doc.get("Istoric")
        else:
            return None
        

    def delete_user(self, username):
        """Delete the user from the database."""
        doc_ref = self.db.collection("Users").document(username)
        doc = doc_ref.get()
        doc_ref.delete()

    def modify_user(self, user: User):
        """A simple first-step method to modify any user field in the database."""
        self.deleteUser(user.username)
        self.addUser(user)

    # TODO : should return an User object
    # def getUser(self, username): 