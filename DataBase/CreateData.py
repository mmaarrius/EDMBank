import os
import bcrypt
import random
import firebase_admin
from firebase_admin import credentials, firestore
from faker import Faker
from datetime import datetime

key_path = os.path.join(os.path.dirname(__file__),"edmbank-7fd19-firebase-adminsdk-fbsvc-97c017e5cd.json")

cred = credentials.Certificate(key_path)

firebase_admin.initialize_app(cred)

db = firestore.client()

fake = Faker()

# Cream 50 de utilizatori random
# contul fiecarui utilizator are:
# nume  parola  nr card(16cifre) CVV data de expirare

for i in range(50):
    UserName = fake.name()
    email = UserName + "@gmail.com"
    email = email.replace(" ","")
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

    Sum = random.randrange(1, 1000)

    Password = random.randrange(10**6,10**7)
    Password_bytes = str(Password).encode()
    salt = bcrypt.gensalt()
    Password = bcrypt.hashpw(Password_bytes, salt)
    Password = Password.decode()

    user_data = {
        "Name" : UserName,
        "Password_hash" : Password,
        "Card_Number" : CardDigit,
        "CVV" : CVV,
        "Expiry_date" : expiry_date,
        "Sold" : Sum,
        "Email" : email,
        "Istoric" : []
    }
    db.collection("Users").document(UserName).set(user_data)