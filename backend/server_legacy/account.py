from flask import Blueprint, request, redirect, jsonify
from authentication import generateToken, checkToken

account_bp = Blueprint("account_bp", __name__)

@account_bp.route("/signup", methods = ['GET'])
def signup():
    return "non funzionante"
    
@account_bp.route("/login", methods = ['GET'])
def login():
    user_dict = {"username": request.args.get("username"), "password": request.args.get("password")}
    token = generateToken(user_dict)
    return redirect("https://admin.progettochearia.it/login_redirect?token="+ token)

@account_bp.route("/checktoken", methods = ['GET'])
def checkauth():
    user = checkToken(request.args.get("token"))
    if user:
        return jsonify(user)

