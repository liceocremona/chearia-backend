from flask import Blueprint, request, jsonify
from authentication import checkToken
import requests
from loadenv import FIREBASE_TOKEN

private_bp = Blueprint("private_bp", __name__)

@private_bp.route("/set_alarm", methods = ['GET'])
def alarm():
    user = checkToken(request.args.get("token"))
    if user:
        allarm_status_req = requests.get("https://olimpiadirobotica-2021-default-rtdb.europe-west1.firebasedatabase.app/db4/allarm/status.json?auth="+ FIREBASE_TOKEN)
        if int(allarm_status_req.text) == 0:
            body = 1
        elif int(allarm_status_req.text) == 1:
            body = 0
        set_state = requests.put("https://olimpiadirobotica-2021-default-rtdb.europe-west1.firebasedatabase.app/db4/allarm/status.json?auth="+ FIREBASE_TOKEN, data=str(body))
        set_state = requests.patch("https://olimpiadirobotica-2021-default-rtdb.europe-west1.firebasedatabase.app/db4/allarm.json?auth="+ FIREBASE_TOKEN, data='{"action":"sicuro"}')
        if set_state.text:
            return set_state.text
    else:
        return "failed"

@private_bp.route("/get_alarm", methods = ['GET'])
def get_alarm():
    user = checkToken(request.args.get("token"))
    if user:
        allarm_status_req = requests.get("https://olimpiadirobotica-2021-default-rtdb.europe-west1.firebasedatabase.app/db4/allarm/status.json?auth="+ FIREBASE_TOKEN)
        return allarm_status_req.text
    else:
        return "failed"

@private_bp.route("/get_alarm_stat", methods = ['GET'])
def get_alarm_state():
    user = checkToken(request.args.get("token"))
    if user:
        allarm_status_req = requests.get("https://olimpiadirobotica-2021-default-rtdb.europe-west1.firebasedatabase.app/db4/allarm/action.json?auth="+ FIREBASE_TOKEN)
        return allarm_status_req.text
    else:
        return "failed"

@private_bp.route("/set_balloon", methods = ['GET'])
def set_ballon():
    user = checkToken(request.args.get("token"))
    if user:
        balloon_status = requests.get("https://olimpiadirobotica-2021-default-rtdb.europe-west1.firebasedatabase.app/db4/pallone/stato.json")
        ballon_action = requests.get("https://olimpiadirobotica-2021-default-rtdb.europe-west1.firebasedatabase.app/db4/pallone/azione.json")
        s = str(balloon_status.text)
        a = str(ballon_action.text)
        if (s == '"terra"'):
            req = requests.patch("https://olimpiadirobotica-2021-default-rtdb.europe-west1.firebasedatabase.app/db4/pallone.json?auth="+FIREBASE_TOKEN, data='{"azione":"aria"}')
            return jsonify(req.text)
        elif s == '"aria"':
            req = requests.patch("https://olimpiadirobotica-2021-default-rtdb.europe-west1.firebasedatabase.app/db4/pallone.json?auth="+FIREBASE_TOKEN, data='{"azione":"terra"}')
            return jsonify(req.text)
        else:
            return "failed"
    else:
        return "failed_h"