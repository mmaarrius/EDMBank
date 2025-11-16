import os
import firebase_admin
from firebase_admin import credentials, firestore

key_path = os.path.join(os.path.dirname(__file__),"edmbank-7fd19-firebase-adminsdk-fbsvc-97c017e5cd.json")

cred = credentials.Certificate(key_path)

# Checks if the app was already initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
