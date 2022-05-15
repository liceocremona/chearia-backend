from flask import Flask, redirect
from flask_cors import CORS
from account import account_bp
from private import private_bp
from board import board_bp
from resources import resources_bp

#init Flask app
app = Flask(__name__)
CORS(app,
origins=["https://progettochearia.it",
 "https://web.progettochearia.it",
 "https://admin.progettochearia.it"]
)

app.register_blueprint(account_bp, url_prefix="/account")
app.register_blueprint(private_bp, url_prefix="/private")
app.register_blueprint(board_bp, url_prefix="/board")
app.register_blueprint(resources_bp, url_prefix="/resources")

@app.get('/', methods = ['GET'])
def get():
    return redirect("https://progettochearia.it", 302)


if __name__ == "__main__":
    app.run()