from datetime import datetime
from fastapi import APIRouter, HTTPException, Response, Path, Query
import os
from pytz import timezone
from bson.codec_options import CodecOptions

import sys
sys.path.append("..")
from loadenv import STORAGE
from db_connect import client
GRAPH_BASEURL = "https://storage.progettochearia.it/graph/"
#from ..use_regex import timestamp1_regex, timestamp2_regex, dataid_regex
#from ..loadenv import STORAGE

router = APIRouter()
db1 = client.measurements1
rome_tz = timezone('Europe/Rome')

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
                
@router.get("/datas/{dataid}")
async def list_all_data(dataid: str = Path(..., regex="(itwork|example|CO|altitude|humidity|ozone|pressure|temperature)"), gte: str = Query(...), lte: str = Query(...)):
    
    gte_time = datetime.strptime(gte, "%Y-%m-%d_%H:%M:%S")
    lte_time = datetime.strptime(lte, "%Y-%m-%d_%H:%M:%S")
    gte_time = rome_tz.localize(gte_time)
    lte_time = rome_tz.localize(lte_time)
    data_collection = db1[dataid].with_options(codec_options=CodecOptions(
    tz_aware=True,
    tzinfo=rome_tz))
    datas = data_collection.find(
    {
        "timestamp":{
            "$gte": gte_time,
            "$lte": lte_time
        }
    })
    print(str(datas))
    return "datas"
# @router.get("/datas")
# async def listdatas(start: str = Query(..., min_length=10, max_length=19), end: Optional[str] = Query(None, min_length=10, max_length=19), type: List[str] = Query(...)):
#     start_timestamp = start.split("_")
#     if end:
#         end_timestamp = end.split("_")
    
#     return {"start": start_timestamp, "end": str(end_timestamp), "type": type_data_list}