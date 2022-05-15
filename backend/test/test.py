import os
STORAGE = ""
def liststorage():

    datas_id = []
    timestamps = ["27-04-2022"]
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
    return returngraph


if __name__ == "__main__":
        for file in liststorage():
            print(file)