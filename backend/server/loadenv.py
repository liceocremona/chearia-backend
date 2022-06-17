from dotenv import load_dotenv
import os
load_dotenv()

STORAGE= os.getenv("STORAGE")
KEY = bytes(os.getenv("KEY"), "utf-8")
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")