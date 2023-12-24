import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("A:\\Proyectos\\Backend_EC\\Edge-Airsense\\credentials.json")
firebase_admin.initialize_app(cred)

#instancia de Firebase Store
db = firestore.client()