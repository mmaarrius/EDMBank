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
        sum = user.balance
    
        Password_bytes = str(password).encode()
        salt = bcrypt.gensalt()
        Password = bcrypt.hashpw(Password_bytes, salt)
        Password = Password.decode()
        expiry_date = user.card.expiry_date


        user_data = {
             "Name" : username,
             "Password_hash" : Password,
             "Card_Number" : CardDigit,
             "CVV" : CVV,
             "Expiry_date" : expiry_date,
             "Sold" : sum,
             "Email" : email,
             "Istoric" : history
         }
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
        self.delete_user(user.credentials.username)
        self.add_user(user)

    def get_user(self, username):
        doc_ref = self.db.collection("Users").document(username)
        doc = doc_ref.get()
        data = doc.to_dict

        email = data.get("Email")
        balance = data.get("Sold")
        hashed_pass = data.get("Password_hash")
        cardNr = data.get("Card_Number")
        cvv = data.get("CVV")
        exp_date = data.get("Expiry_date")
        history = data.get("Istoric")

        credentials = UserCredentials(
            username = username,
            password = hashed_pass,
            email = email
        )

        card = Card(
            number = cardNr,
            cvv = cvv,
            expiry_date = exp_date
        )
        history_formated = PaymentsHistory()

        User(
            credentials=credentials,
            balance=balance,
            payment_history=history_formated,
            card=card
        )

        return User
