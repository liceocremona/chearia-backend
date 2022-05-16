from datetime import datetime
from email.policy import default
from lib2to3.pgen2 import grammar
from nis import match
from fastapi import APIRouter, HTTPException, Response, Path, Query, Body
from pydantic import BaseModel, Field
from typing import Union, List
import os
from pytz import timezone
from bson.codec_options import CodecOptions

import sys
sys.path.append("..")
from loadenv import STORAGE
from db_connect import client
from use_regex import timestamp1_regex, dataid_regex_str, timestamp_date_regex, timestamp_time_regex, timestamp_date_regex_str
GRAPH_BASEURL = "https://storage.progettochearia.it/graph/"
#from ..use_regex import timestamp1_regex, timestamp2_regex, dataid_regex
#from ..loadenv import STORAGE

router = APIRouter()
db1 = client.measurements1
rome_tz = timezone('Europe/Rome')


class DateRange(BaseModel):
    gte: str = Field(min_length=10, max_length=19, description="The date to start from")
    lte: str = Field(min_length=10, max_length=19, description="The date to end to")

class DateUnique(BaseModel):
    date: str = Field(min_length=10, max_length=19, description="The date to start from")
class DateQuery(BaseModel):
    date_range: Union[DateRange, None] = None
    date_unique: Union[DateUnique, None] = None


def map_storage(storage):
    if not storage or len(storage) == 0:
        raise Exception("Storage not found")
    graphs_url = []
    for root, dirs, files in os.walk(storage):
        for file in files:
            if file.endswith(".svg"):
                base_path = root.replace(STORAGE, "")
                if base_path.startswith("/"):
                    base_path = base_path[1:]  
                file_info = file.split("_")
                if not 3 <= len(file_info) <= 6:
                    continue
                file_title = file_info[0]
                file_meta = file_info[1]
                if len(file_info) == 3:
                    if timestamp_date_regex.match(file_info[2]):
                        file_date_start = file_info[2] + "_00:00:00"
                        file_date_end = file_info[2] + "_23:59:59"
                    else:
                        continue
                elif len(file_info) == 4:
                    if timestamp_date_regex.match(file_info[2]) and timestamp_date_regex.match(file_info[3]):
                        file_date_start = file_info[2] + "_00:00:00"
                        file_date_end = file_info[3] + "_23:59:59"
                    else:
                        continue
                elif len(file_info) == 5:
                    if timestamp_date_regex.match(file_info[2]):
                        if timestamp_date_regex.match(file_info[3]):
                            if timestamp_time_regex.match(file_info[4]):
                                file_date_start = file_info[2]+"_00:00:00"
                                file_date_end = file_info[3]+"_"+file_info[4]
                            else:
                                continue
                        elif timestamp_time_regex.match(file_info[3]):
                            if timestamp_date_regex.match(file_info[4]):
                                file_date_start = file_info[2]+"_"+file_info[3]
                                file_date_end = file_info[4]+"_23:59:59"
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                elif len(file_info) == 6:
                    if timestamp1_regex.match(file_info[2] + "_" + file_info[3]) and timestamp1_regex.match(file_info[4] + "_" + file_info[5]):
                        file_date_start = file_info[2] + "_" + file_info[3]
                        file_date_end = file_info[4] + "_" + file_info[5]
                    else:
                        continue
                else:
                    continue

                file_date_start = datetime.strptime(file_date_start, "%Y-%m-%d_%H:%M:%S")
                file_date_end = datetime.strptime(file_date_end, "%Y-%m-%d_%H:%M:%S")
                file_date_start = rome_tz.localize(file_date_start)
                file_date_end = rome_tz.localize(file_date_end)
                graphs_url.append({
                    "file": file,
                    "title": file_title,
                    "meta": file_meta,
                    "dates": {
                        "start": file_date_start,
                        "end": file_date_end
                    },
                })
    return graphs_url
                        

                
                

@router.get("/graph/all")
async def list_all_graphs(type: str = None):
    if not STORAGE or len(STORAGE) == 0:
        raise HTTPException(status_code=503, detail="No resources available")
    graphs_url_list = []
    for root, dirs, files in os.walk(STORAGE):
        for file in files:
            if file.endswith(".svg"):
                graph = os.path.join(root, file)
                graph = graph.replace(STORAGE, "");
                if graph.startswith("/"):
                    root = root[1:]
                graph_url = GRAPH_BASEURL + graph
                graphs_url_list.append(graph_url)
    if type == "html":
        html_return = ""
        for graph_url in graphs_url_list:
            html_return += "<a href='" + graph_url + "'>" + graph_url + "</a><br>"
        return Response(content=html_return, media_type="text/html")
    return graphs_url_list

@router.post("/graph/query")
async def query_graph(
    dataid: List[str] = Query(default=["itwork"]),
    gte: str = Query(None, min_length=10, max_length=19),
    lte: str = Query(None, min_length=10, max_length=19),
    unique: str = Query(None, regex=timestamp_date_regex_str,min_length=10, max_length=10),
    ):

    return []

    

    
                
@router.get("/datas/{dataid}")
async def list_all_data(
    dataid: str = Path(..., regex=dataid_regex_str),
    gte: str = Query(None, min_length=10, max_length=19), 
    lte: str = Query(None, min_length=10, max_length=19), 
    type: str = Query(None, regex="(html|json)")
    ):
    if not gte and not lte:
        raise HTTPException(status_code=400, detail="Bad request, insert at least one time parameter")
    fetch_dict = {
        "timestamp":{}
    }
    # {
    #     "timestamp":{
    #         "$gte": gte_time,
    #         "$lte": lte_time
    #     }
    # }
    if gte:
        if len(gte.split("_")) == 1:
            gte = gte + "_00:00:00"
        if not timestamp1_regex.match(gte):
            raise HTTPException(status_code=400, detail="Invalid gte timestamp")
        gte_time = datetime.strptime(gte, "%Y-%m-%d_%H:%M:%S")
        gte_time = rome_tz.localize(gte_time)
        fetch_dict["timestamp"]["$gte"] = gte_time
    if lte:
        if len(lte.split("_")) == 1:
            lte = lte + "_23:59:59"
        if not timestamp1_regex.match(lte):
            raise HTTPException(status_code=400, detail="Invalid lte timestamp")
        lte_time = datetime.strptime(lte, "%Y-%m-%d_%H:%M:%S")
        lte_time = rome_tz.localize(lte_time)
        fetch_dict["timestamp"]["$lte"] = lte_time


    data_collection = db1[dataid].with_options(codec_options=CodecOptions(
    tz_aware=True,
    tzinfo=rome_tz))
    datas = data_collection.find(fetch_dict)
    datas_list  = []
    for data in datas:
        datas_list.append({
            "time": data["timestamp"].strftime("%Y-%m-%d_%H:%M:%S"),
            "value": data["value"],
            "metadata": data["metadata"]
        })
    if type == "html":
        html_return = ""
        for data in datas_list:
            html_return += data["time"] + "&nbsp;&nbsp;&nbsp;&nbsp;" + str(data["value"]) + "<br>"
        return Response(content=html_return, media_type="text/html")
    return datas_list



# @router.get("/datas")
# async def listdatas(start: str = Query(..., min_length=10, max_length=19), end: Optional[str] = Query(None, min_length=10, max_length=19), type: List[str] = Query(...)):
#     start_timestamp = start.split("_")
#     if end:
#         end_timestamp = end.split("_")
    
#     return {"start": start_timestamp, "end": str(end_timestamp), "type": type_data_list}