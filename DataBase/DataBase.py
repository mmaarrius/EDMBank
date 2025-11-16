import bcrypt
import os
import bcrypt
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from faker import Faker
from datetime import datetime

class Database:
    def __init__(self):
        self.initializareBazaDate()

    def initializareBazaDate(self):
        key_path = os.path.join(os.path.dirname(__file__),"edmbank-7fd19-firebase-adminsdk-fbsvc-97c017e5cd.json")
        if not firebase_admin._apps:
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def adaugaUtilizator(self, username, Password, email, sum):
        CardDigit = random.randrange(10**15,10**16-1)
        CVV = random.randrange(10**2,10**3)
        current_year = datetime.now().year
        year_first = current_year + 1
        year_last = current_year + 20
        rand_year = random.randrange(year_first, year_last)
        rand_month = random.randrange(1,12)
        if rand_month < 10:
            expiry_date = "0" + str(rand_month) + "/" + str(rand_year%100) 
        else:
            expiry_date = str(rand_month) + "/" + str(rand_year%100)
        Password_bytes = str(Password).encode()
        salt = bcrypt.gensalt()
        Password = bcrypt.hashpw(Password_bytes, salt)
        Password = Password.decode()

        user_data = {
            "Name" : username,
            "Password_hash" : Password,
            "Card_Number" : CardDigit,
            "CVV" : CVV,
            "Expiry_date" : expiry_date,
            "Sold" : sum,
            "Email" : email,
            "Istoric" : []
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

    def adaugaIstoric(self, username, amount, receiver):
        doc_ref = self.db.collection("Users").document(username)
        doc = doc_ref.get()

        entry = "You have sent " + str(amount) + " to " + receiver+ "."
        doc_ref.update({"Istoric" : firestore.ArrayUnion([entry])})

    def extrageDate(self, username, date):
        doc_ref = self.db.collection("Users").document(username)
        doc = doc_ref.get()
        #date este o valoare care indica
        #field ul care urmeaza sa fie returnat
        # card - nr =1, cvv = 2, expiry date = 3, sold = 4, email =5, istoric = 6
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
        

    def stergeUtilizator(self, username):
        doc_ref = self.db.collection("Users").document(username)
        doc = doc_ref.get()
        doc_ref.delete()

    def modifica(self, username, varianta, modificator):
        doc_ref = self.db.collection("Users").document(username)
        doc = doc_ref.get()
        if varianta == 1: # vrea sa modifice username
            data = doc.to_dict()
            data["Name"] = modificator
            self.db.collection("Users").document(modificator).set(data)
            doc_ref.delete()

        if varianta == 2: # vrea sa modifice email
            doc_ref.update({"Email" : modificator})