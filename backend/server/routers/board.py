from fastapi import APIRouter, Path, Body, HTTPException
from fastapi.responses import PlainTextResponse
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from pytz import timezone
from bson.codec_options import CodecOptions

import sys
sys.path.append("..")
from loadenv import KEY
from db_connect import client

rome_tz = timezone('Europe/Rome')
db1 = client.measurements1
router = APIRouter()

class Data(BaseModel):
    datavalue: float = Field(..., description="The value of data from sensor")
    timestamptz: Optional[str] = Field(None, description="The timzone to use to calculate the timestamp", min_length=2 ,max_length=3)
    key: bytes = Field(..., description="The key for authenticate request", min_length=32, max_length=32)


@router.get("/time", response_class=PlainTextResponse)
async def gettime():
    time = datetime.now(rome_tz)
    return time.strftime('%H-%M')

@router.get("/timems", response_class=PlainTextResponse)
@router.get("/timems/{tz}", response_class=PlainTextResponse)
async def gettimems(tz: str = None):
    if tz:
        now_timezone = timezone('ETC/GMT'+tz)
    else:
        now_timezone = rome_tz
    
    now = datetime.now(now_timezone)
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    ms_from_midnight = ((now - midnight).seconds) * 1000
    return str(ms_from_midnight)


@router.get("/time/hour", response_class=PlainTextResponse)
async def gettime_h():
    time = datetime.now(rome_tz)
    return time.strftime('%H')


@router.get("/time/min", response_class=PlainTextResponse)
async def gettime_min():
    time = datetime.now(rome_tz)
    return time.strftime('%M')


@router.get("/date", response_class=PlainTextResponse)
@router.get("/date/{tz}", response_class=PlainTextResponse)
async def getdate(tz: str = None):
    if tz:
        now_timezone = timezone('ETC/GMT'+tz)
    else:
        now_timezone = rome_tz
    time = datetime.now(now_timezone)
    return time.strftime('%Y-%m-%d')


@router.put("/putdata/{dataid}", response_class=PlainTextResponse)
async def putdata(dataid: str = Path(..., regex="(itwork|example|CO|altitude|humidity|ozone|pressure|temperature)"), data: Data = Body(...)):
    if not data.key == KEY:
        raise HTTPException(status_code=403, detail="Wrong key")
    if data.timestamptz:
        now_timezone = timezone('ETC/GMT'+data.timestamptz)
    else:
        now_timezone = rome_tz
    now = datetime.now(now_timezone)
    data_collection = db1[dataid].with_options(codec_options=CodecOptions(
    tz_aware=True,
    tzinfo=now_timezone))
    try:
        data_collection.insert_one({
        "metadata": {
            "id": dataid,
        },
        "value": data.datavalue,
        "timestamp": now
    })
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    return "ok"