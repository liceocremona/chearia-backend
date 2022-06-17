from flask import Blueprint
from datetime import datetime
from pytz import timezone

rome_tz = timezone('Europe/Rome')

board_bp = Blueprint("board_bp", __name__)

@board_bp.route("/time", methods = ['GET'])
def gettime():
    
    time = datetime.now(rome_tz)
    return time.strftime('%H-%M')

@board_bp.route("/timems")
@board_bp.route("/timems/<tz>")
def gettimems(tz=None):
    if tz:
        now_timezone = timezone('ETC/GMT'+tz)
    else:
        now_timezone = rome_tz
    
    now = datetime.now(now_timezone)
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    ms_from_midnight = ((now - midnight).seconds) * 1000
    return str(ms_from_midnight)




@board_bp.route("/time/hour", methods = ['GET'])
def gettime_h():
    time = datetime.now(rome_tz)
    return time.strftime('%H')

@board_bp.route("/time/min", methods = ['GET'])
def gettime_min():
    time = datetime.now(rome_tz)
    return time.strftime('%M')

@board_bp.route("/date", methods = ['GET'])
@board_bp.route("/date/<tz>", methods = ['GET'])
def getdate(tz=None):
    if tz:
        now_timezone = timezone("ETC/GMT"+tz)
    else:
        now_timezone = rome_tz
    time = datetime.now(now_timezone)
    return time.strftime('%Y-%m-%d')