#connection to mongodb
import pymongo

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = mongo_client["mydatabase"]
mycol = mydb["customers"]

myquery = { "address": "Park Lane 38" }

mydoc = mycol.find(myquery)

for x in mydoc:
  print(x)
