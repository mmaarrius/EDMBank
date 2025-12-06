import bcrypt
import os
import bcrypt
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1 import FieldFilter
from faker import Faker
from datetime import datetime
from user_management.user import User
from user_management.credit_card import Card
from user_management.user_credentials import UserCredentials
from user_management.payment_details import PaymentsHistory
from user_management.payment_details import Payment
from user_management.request import Request
from exceptions import *

class Database:
    def __init__(self):
        self.init_dadabase()

    def init_dadabase(self):
        key_path = os.path.join(os.path.dirname(__file__),"edmbank-7fd19-firebase-adminsdk-fbsvc-97c017e5cd.json")
        if not firebase_admin._apps:
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def history_to_databse_format(self, history : PaymentsHistory):
        hist = []
        for payment in history.history:
            amount = payment.amount
            rec = payment.receiver
            send = payment.sender
            sentence = (f"{send} -> {amount} -> {rec}")
            hist.append(sentence)
        return hist
    
    def database_to_class_format(self, history_sentence : list[str]) -> PaymentsHistory:
        history = PaymentsHistory()
        for sentence in history_sentence:
            try:
                sender, amount, receiver = sentence.split(" -> ")
                payment = Payment(
                    amount = float(amount),
                    sender = sender,
                    receiver = receiver
                )
                history.add_payment(payment)
            except ValueError:
                continue
        return history

    def add_user(self, user : User):
        """Add a new user to the database."""
        password = user.credentials.password
        username = user.credentials.username
        CardDigit = user.card.number
        CVV = user.card.cvv
        IBAN = user.card.IBAN
        email = user.credentials.email
        history = user.payment_history
        history = self.history_to_databse_format(history)
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
             "Iban" : IBAN,
             "History" : history
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
            return doc.get("History")
        elif date == 7:
            return doc.get("Iban")   
        else:
            return None
        

    def delete_user(self, username):
        """Delete the user from the database."""
        doc_ref = self.db.collection("Users").document(username)
        doc = doc_ref.get()
        doc_ref.delete()

    def modify_user(self, user: User):
        """Update existing user fields safely."""
        user_data = {
            "Name": user.credentials.username,
            "Password_hash": user.credentials.password,
            "Card_Number": user.card.number,
            "CVV": user.card.cvv,
            "Expiry_date": user.card.expiry_date,
            "Sold": user.balance,
            "Email": user.credentials.email,
            "Iban": user.card.IBAN,
            "History": self.history_to_databse_format(user.payment_history)
        }
        self.db.collection("Users").document(user.credentials.username).update(user_data)

    def listen_to_user(self, username, callback):
        """Listen to changes on a user document."""
        doc_ref = self.db.collection("Users").document(username)
        return doc_ref.on_snapshot(callback)

    def get_user(self, username):
        doc_ref = self.db.collection("Users").document(username)
        doc = doc_ref.get()

        if not doc.exists:
            raise AccountNotFoundError(f"Account '{username}' does not exist.")
        
        data = doc.to_dict()
        return self._create_user_from_data(username, data)

    def get_user_by_iban(self, iban: str) -> User:
        users_ref = self.db.collection("Users")
        query = users_ref.where(filter=FieldFilter("Iban", "==", iban)).get()
        
        if not query:
            raise AccountNotFoundError(f"Account with IBAN '{iban}' does not exist.")
        
        doc = query[0]
        data = doc.to_dict()
        username = doc.id # or data.get("Name")
        return self._create_user_from_data(username, data)

    def _create_user_from_data(self, username, data):
        email = data.get("Email")
        balance = data.get("Sold")
        hashed_pass = data.get("Password_hash")
        cardNr = data.get("Card_Number")
        cvv = data.get("CVV")
        IBAN = data.get("Iban")
        exp_date = data.get("Expiry_date")
        history = data.get("History")
        history = self.database_to_class_format(history)

        credentials = UserCredentials(
            username = username,
            password = hashed_pass,
            email = email
        )

        card = Card(
            number = cardNr,
            cvv = cvv,
            IBAN = IBAN,
            expiry_date=exp_date
        )

        user = User(
            credentials=credentials,
            balance=balance,
            payment_history=history,
            card=card
        )

        return user
        

    def card_exists(self, card_number: str) -> bool:
        """
        Check if a generated card number already exists in the database.
        """
        users_ref = self.db.collection("Users")
        query = users_ref.where(filter=FieldFilter("Card_Number", "==", card_number)).get()

        # If query is not empty, card exists
        return len(query) > 0

    def add_request(self, request: Request):
        """
        Adds a support request to the 'Requests' collection in Firestore.
        """
        try:
            requests_ref = self.db.collection("Requests")
            requests_ref.document(request.request_id).set(request.to_dict())
        except Exception as e:
            raise RequestError(f"Failed to add request to database: {e}")

