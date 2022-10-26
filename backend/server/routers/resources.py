from use_regex import timestamp1_regex, dataid_regex_str, timestamp_date_regex, timestamp_time_regex, timestamp_date_regex_str, timestamp_datetime_str1, timestamp_date_str2
from db_connect import client
from loadenv import STORAGE
from event_manager import announcer
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Response, Path, Query, Body, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from typing import Union, List
import os
from pytz import timezone
from bson.codec_options import CodecOptions
from sse_starlette.sse import EventSourceResponse
import asyncio

import sys
sys.path.append("..")
GRAPH_BASEURL = "https://storage.progettochearia.it/graph/"
STORAGE = "/srv/www/media/graph"
#from ..use_regex import timestamp1_regex, timestamp2_regex, dataid_regex
#from ..loadenv import STORAGE

router = APIRouter()
db1 = client.measurements1
rome_tz = timezone('Europe/Rome')


class DateRange(BaseModel):
    gte: str = Field(min_length=10, max_length=19,
                     description="The date to start from")
    lte: str = Field(min_length=10, max_length=19,
                     description="The date to end to")


class DateUnique(BaseModel):
    date: str = Field(min_length=10, max_length=19,
                      description="The date to start from")


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

                file_date_start = datetime.strptime(
                    file_date_start, "%Y-%m-%d_%H:%M:%S")
                file_date_end = datetime.strptime(
                    file_date_end, "%Y-%m-%d_%H:%M:%S")
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


@router.get("/graph/all", tags=["resources"])
async def list_all_graphs(type: str = None):
    if not STORAGE or len(STORAGE) == 0:
        raise HTTPException(status_code=503, detail="No resources available")
    graphs_url_list = []
    for root, dirs, files in os.walk(STORAGE):
        for file in files:
            if file.endswith(".svg"):
                graph = os.path.join(root, file)
                graph = graph.replace(STORAGE, "")
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


@router.post("/graph/query", tags=["resources"], deprecated=True)
async def query_graph(
    dataid: List[str] = Query(default=["itwork"]),
    gte: str = Query(None, min_length=10, max_length=19),
    lte: str = Query(None, min_length=10, max_length=19),
    unique: str = Query(None, regex=timestamp_date_regex_str,
                        min_length=10, max_length=10),
):

    return []

# @router.get("/datas", include_in_schema=False)
# async def datas_default():
#     return RedirectResponse("https://api.progettochearia.it/v1/docs#/resources/list_all_data_resources_datas_get")


@router.get("/datas", tags=["resources"])
async def list_all_data(

    dataid: List[str] = Query(..., regex=dataid_regex_str),
    gte: str = Query(None, min_length=10, max_length=19,
                     regex=timestamp_datetime_str1,
                     title="Data iniziale",
                     description="Data d'inizio, ex: 2022-05-15_10:24:00 or 2022-05-15",
                     ),
    lte: str = Query(None, min_length=10, max_length=19,
                     regex=timestamp_datetime_str1,
                     title="Data finale",
                     description="Data di fine, ex: 2022-10-15_16:12:00 or 2022-10-15",
                     ),
    day: str = Query(None, min_length=10, max_length=10,
                     regex=timestamp_date_str2,
                     title="Giorno singolo",
                     description="Giorno singolo, ex: 2022-10-15",
                     ),                 
    type: str = Query(None, regex="(html|json)"),
    sort: str = Query(None, regex="(asc|desc)"),
):

    if not gte and not lte and not day:
        raise HTTPException(
            status_code=400, detail="Bad request, insert at least one time parameter")

    sort = sort if sort else "asc"  # variable to order of the data

    fetch_dict = {
        "timestamp": {}
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
        gte_time = datetime.strptime(gte, "%Y-%m-%d_%H:%M:%S")
        gte_time = rome_tz.localize(gte_time)
        fetch_dict["timestamp"]["$gte"] = gte_time
    if lte:
        if len(lte.split("_")) == 1:
            lte = lte + "_23:59:59"
        lte_time = datetime.strptime(lte, "%Y-%m-%d_%H:%M:%S")
        lte_time = rome_tz.localize(lte_time)
        fetch_dict["timestamp"]["$lte"] = lte_time
    if not gte and not lte and day:
        gte_time = datetime.strptime(day, "%Y-%m-%d")
        gte_time = rome_tz.localize(gte_time)
        lte_time = gte_time + timedelta(days=1)
        fetch_dict["timestamp"]["$gte"] = gte_time
        fetch_dict["timestamp"]["$lte"] = lte_time

    return_dict = {}

    for key in dataid:
        data_collection = db1[key].with_options(codec_options=CodecOptions(
        tz_aware=True,
        tzinfo=rome_tz))

        try:
            datas = None
            datas = data_collection.find(fetch_dict)
            datas_list = []
            for data in datas:
                try:
                    item_data = {
                    "time": data["timestamp"].strftime("%Y-%m-%d_%H:%M:%S"),
                    "value": data["value"],
                    "metadata": data["metadata"]}
                    datas_list.append(item_data)
                except KeyError:
                    pass
            if sort == "asc":
                datas_list.reverse()
            return_dict[key] = datas_list
            
        except Exception as error:
            print(str(error) + "\n" + str(datas))
            raise HTTPException(
                status_code=500, detail="Error while retrieving data from DB")

    

    if type == "html":#genera una lista dei dati visualizzabile in html
        html_return = ""
        n_iter = 0
        html_return += "<table><thead><tr>"
        for key in return_dict:
            if len(return_dict[key]) > n_iter:
                n_iter = len(return_dict[key])
            html_return += "<th>" + key + "</th>"
        html_return += "</tr></thead><tbody>"
        for i in range(n_iter):
            html_return += "<tr>"
            for key in return_dict:
                if len(return_dict[key]) > i:
                    html_return += "<td style='padding-right: 3em;'>{0}:     {1}</td>".format(return_dict[key][i]["time"], str(return_dict[key][i]["value"]))
                else:
                    html_return += "<td></td>"
            html_return += "</tr>"
        html_return += "</tbody></table>"
        return Response(content=html_return, media_type="text/html")
    return return_dict

@router.get("/datas/last", tags=["resources"])
async def list_last_data(
    dataid: List[str] = Query(..., regex=dataid_regex_str),
    type: str = Query(None, regex="(html|json)"),
):

    return_dict = {}

    for key in dataid:
        data_collection = db1[key].with_options(codec_options=CodecOptions(
        tz_aware=True,
        tzinfo=rome_tz))

        try:
            datas = None
            datas = data_collection.find().sort("timestamp", -1).limit(1)

            for data in datas:
                try:
                    item_data = {
                    "time": data["timestamp"].strftime("%Y-%m-%d_%H:%M:%S"),
                    "value": data["value"],
                    "metadata": data["metadata"]}
                    return_dict[key] = item_data
                    break
                except KeyError:
                    pass
            
        except Exception as error:
            print(str(error) + "\n" + str(datas))
            raise HTTPException(
                status_code=500, detail="Error while retrieving data from DB")

    if type == "html":
        html_return = ""
        html_return += "<table><thead><tr>"
        for key in return_dict:
            html_return += "<th>" + key + "</th>"
        html_return += "</tr></thead><tbody>"
        html_return += "<tr>"
        for key in return_dict:
            html_return += "<td style='padding-right: 3em;'>{0}:     {1}</td>".format(return_dict[key]["time"], str(return_dict[key]["value"]))
        html_return += "</tr>"
        html_return += "</tbody></table>"
        return Response(content=html_return, media_type="text/html")
    return return_dict


@router.get("/datas_stream", tags=["resources"])
async def datas_streams(request: Request):
    """
    Questa funzione restituisce uno streaming dei dai che arrivano dai sensori
    """
    async def event_generator():
        datas = await announcer.listen()
        while True:
            if await request.is_disconnected():
                break
            data = await datas.get()
            print(data)
            yield data
            
    return EventSourceResponse(event_generator())
# @router.get("/datas")
# async def listdatas(start: str = Query(..., min_length=10, max_length=19), end: Optional[str] = Query(None, min_length=10, max_length=19), type: List[str] = Query(...)):
#     start_timestamp = start.split("_")
#     if end:
#         end_timestamp = end.split("_")

#     return {"start": start_timestamp, "end": str(end_timestamp), "type": type_data_list}
