import json
import os
import time

with open("client/backend/test/olimpiadirobotica-2021-default-rtdb-export.json") as db_json:
    db_all = json.load(db_json)

db1 = db_all["db1"]
db1_new = {}
print(str(db1))
for data_type in db1:
    db1_new[data_type] = {"data":{}}
    for date in db1[data_type]["data"]:
        new_date = date.split("-")[2] + "-" + date.split("-")[1] + "-" + date.split("-")[0]
        print(data_type)
        print(new_date)
        db1_new[data_type]["data"][new_date] = db1[data_type]["data"][date]
        #del db1_new[data_type]["data"][date]
print(str(db1_new))

db_all["db1"] = db1_new

with open("client/backend/test/updatedb.json", "w") as update_db:
    json.dump(db_all, update_db)