import requests
import jwt
import hashlib
from loadenv import KEY, FIREBASE_TOKEN

def checkLogin(user_dict):#this function check credential
    req = requests.get("https://olimpiadirobotica-2021-default-rtdb.europe-west1.firebasedatabase.app/db3-user.json?auth="+ FIREBASE_TOKEN)
    db = req.json()
    username_s = user_dict["username"]
    pass_hash = hashlib.sha256(str.encode(user_dict["password"])).hexdigest()
    for user in db:
        if username_s==user["username"] and pass_hash==user["password"]:
            return user_dict

def generateToken(user_dict):
    user_dict = checkLogin(user_dict)
    if user_dict:
        return jwt.encode(user_dict, KEY, algorithm="HS256")

def checkToken(dict_token):
    user_dict = jwt.decode(dict_token, KEY, algorithms="HS256")
    if user_dict:
        user_dict = checkLogin(user_dict)
        if user_dict:
            return user_dict