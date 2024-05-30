from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi



mongodb_uri = 'mongodb+srv://mohitashliya:bf2b3XXI6v0SfLtd@cluster0.6veobfq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(mongodb_uri, server_api=ServerApi('1'))
def conncectDB():
    if client: 
            print(client)

