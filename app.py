from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from connection.connectdb import conncectDB, client
from routes.route import router
from routes.route2 import router as router2
from connection.connectdb2 import ping_server
import time

#lifecycle of fastapi app
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifecycle started")
    conncectDB()
    # ping_server()
    yield
    print("lifecycle ended")


app = FastAPI(lifespan= lifespan)

app.include_router(router=router2)

@app.middleware('http')
async def middleware_processing(request: Request, call_next):
    startTime = time.time()
    response = await call_next(request)
    process_time = time.time() - startTime
    response.headers['X-Process-Time'] = str(process_time)
    return response

