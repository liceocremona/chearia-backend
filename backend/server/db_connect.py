from loadenv import MONGO_CONNECTION_STRING
import pymongo
client = pymongo.MongoClient(MONGO_CONNECTION_STRING)

