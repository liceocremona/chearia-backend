from flask import Blueprint, request, jsonify
import os
from use_regex import timestamp1_regex, timestamp2_regex, dataid_regex
from loadenv import STORAGE

resources_bp = Blueprint("resources_bp", __name__)


@resources_bp.route('/datas', methods=["GET"])
def listdatas():
    start_timestamp = request.args.get("start")
    end_timestamp = request.args.get("end")
    single_timestamp = request.args.get("day")
    type_data_list = request.args.getlist("type")
    if not type_data_list:
        return jsonify({"error": "type of data required"}),500
    else:
        for type_data in type_data_list:
            if not dataid_regex.match(str(type_data)):
                type_data_list.remove(type_data)
        if len(type_data) == 0:
            return jsonify({"error": "type of right data required"}),500
    if start_timestamp and end_timestamp:
        # if not timestamp1_regex.match(start_timestamp) or not timestamp1_regex.match(end_timestamp):
        #     return jsonify({"error": "incorrect timestamp format"}),500
        pass
    elif single_timestamp:
        pass
    else:
        return jsonify({"error": "a date or a range of date required"}),500

@resources_bp.route('/liststorage/bytype', methods=['POST'])
def liststoragebytype():
    body = request.json

    datas_id = ["example"]
    timestamps = ["27-04-2022"]
    returngraph = []
    for root, dirs, files in os.walk(STORAGE):
        for file in files:
            if file.endswith(".svg"):
                graph = file.replace(STORAGE, "")
                graph_name = graph.replace(".svg", "")
                data_id = graph_name.split("_")[-1]
                if data_id in datas_id:
                    data_timestamp = graph_name.split("_")[-2]
                    name = graph_name.split("_")[-3]
                    if data_timestamp in timestamps:
                        returngraph.append({
                            "file": graph,
                            "title": name,
                        })
    return jsonify(returngraph)

@resources_bp.route('/liststorage', methods=['POST'])
def liststorage():
    body = request.json
    
    if not "dates" in body.keys():
        return jsonify({"error": "date required"}), 500
    else:
        args_date_list = body["dates"]
        if not len(args_date_list) > 0:
            return jsonify({"error": "date required"}), 500
        else:
            for date_timestamp in args_date_list:
                if not timestamp2_regex.match(date_timestamp):
                    return jsonify({"error": "invalid date"}), 500
            timestamps = args_date_list    

    if not "id" in body.keys():
        datas_id = []
    else:
        if len(body["id"]) == 0:
            datas_id = []
        else:
            datas_id = body["id"]
    
    returngraph = []

    for root, dirs, files in os.walk(STORAGE):
        for file in files:
            if file.endswith(".svg"):
                graph = file.replace(STORAGE, "")
                graph_name = graph.replace(".svg", "")
                data_timestamp = graph_name.split("_")[-1]
                if data_timestamp in timestamps:
                    if len(datas_id) == 0:
                        name = graph_name.split("_")[-3]
                        returngraph.append({
                            "file": graph,
                            "title": name,
                        })
                        continue
                    else:
                        data_id = graph_name.split("_")[-2]
                        
                        if data_id in datas_id:
                            name = graph_name.split("_")[-3]
                            returngraph.append({
                                "file": graph,
                                "title": name,
                            })
    if len(returngraph) == 0:
        return jsonify({"error": "no data found"}), 404
    return jsonify(returngraph), 200