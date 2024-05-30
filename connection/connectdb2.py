import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

async def ping_server():
    uri = 'mongodb+srv://mohitashliya:bf2b3XXI6v0SfLtd@cluster0.6veobfq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
    client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))
    try:
      await client.admin.command('ping')
      print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
        
# asyncio.run(ping_server())