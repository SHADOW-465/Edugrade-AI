"""
Firebase Firestore connection setup.
"""

import firebase_admin
from firebase_admin import credentials, firestore
import os

# Path to service account JSON
cred_path = os.environ.get("FIREBASE_CREDENTIALS_PATH")
if not cred_path:
    raise ValueError("FIREBASE_CREDENTIALS_PATH environment variable not set.")

# Initialize Firebase if not already done
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

# Create Firestore client
db = firestore.client()
