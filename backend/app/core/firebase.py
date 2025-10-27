"""
Firebase Firestore connection setup.
"""

import firebase_admin
from firebase_admin import credentials, firestore
import os

# Path to service account JSON
BASE_DIR = os.path.dirname(os.path.abspath(_file_))
cred_path = os.path.join(BASE_DIR, "serviceAccountKey.json")

# Initialize Firebase if not already done
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

# Create Firestore client
db = firestore.client()
