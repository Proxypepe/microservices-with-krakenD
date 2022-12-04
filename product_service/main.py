from fastapi import FastAPI, Request
from router import router
from fastapi.middleware.cors import CORSMiddleware
from deps import init_tracer
import logging
import mongoengine
import time

app = FastAPI(

)

logger = logging.getLogger(__name__)
DB_NAME = 'mydb'


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    logger.info("Connected to base")
    mongoengine.connect(host=f"mongodb://mongo_product:27017/{DB_NAME}", alias=DB_NAME)


@app.on_event("shutdown")
async def shutdown():
    logger.info("Disconnected to base")
    mongoengine.disconnect(alias=DB_NAME)

init_tracer()
app.include_router(router, prefix='/v1')
