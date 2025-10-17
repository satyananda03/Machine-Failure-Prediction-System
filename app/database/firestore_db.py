from firebase_admin import credentials, firestore, initialize_app
from app.config.config import settings

def init_firebase():
    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
    app = initialize_app(cred)
    return firestore.client(app)

db = init_firebase()