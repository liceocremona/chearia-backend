from dotenv import load_dotenv
import os
load_dotenv()
FIREBASE_TOKEN = os.getenv("FIREBASE_TOKEN")
STORAGE= os.getenv("STORAGE")
KEY = bytes(os.getenv("KEY"), "utf-8")
DB_URL = os.getenv("DB_URL")
DB_DATA  = os.getenv("DB_DATA")