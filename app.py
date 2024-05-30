from fastapi import FastAPI
from contextlib import asynccontextmanager
from connection.connectdb import conncectDB, client
from pymongo.errors import PyMongoError
from routes.route import router
from connection.connectdb2 import ping_server


#lifecycle of fastapi app
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifecycle started")
    conncectDB()
    # ping_server()
    yield
    print("lifecycle ended")


app = FastAPI(lifespan= lifespan)

app.include_router(router=router)

