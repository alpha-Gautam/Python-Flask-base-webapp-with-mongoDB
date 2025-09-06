import firebase_admin
from firebase_admin import credentials, auth
import os
from dotenv import load_dotenv


# Firebase configuration - Replace with your actual Firebase config

load_dotenv()

firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID")
}

# Initialize Firebase Admin SDK
try:
    if not firebase_admin._apps:
        
        if os.path.exists('/etc/secrets/serviceAccountKey.json'):
            service_key_path = '/etc/secrets/serviceAccountKey.json'
        else:
            service_key_path = './serviceAccountKey.json'

        if os.path.exists(service_key_path):
            cred = credentials.Certificate(service_key_path)
            firebase_admin.initialize_app(cred)
        else:
            print("Firebase service account key not found. Please add serviceAccountKey.json")
except Exception as e:
    print(f"Firebase initialization error: {e}")

def verify_firebase_token(id_token):
    """Verify Firebase ID token"""
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(f"Token verification failed: {e}")
        return None

def get_user_info(uid):
    """Get user information by UID"""
    try:
        user = auth.get_user(uid)
        return {
            'uid': user.uid,
            'email': user.email,
            'display_name': user.display_name,
            'email_verified': user.email_verified
        }
    except Exception as e:
        print(f"Error getting user info: {e}")
        return None
