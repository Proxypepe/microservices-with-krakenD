import time
import logging

from fastapi import FastAPI, Request
from router import router
from fastapi.middleware.cors import CORSMiddleware
import mongoengine

from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Summary, Counter
from deps import init_tracer

app = FastAPI(

)

logger = logging.getLogger(__name__)
DB_NAME = 'mydb'
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
total_requests = Counter('total_requests', 'Total requests counter')
total_service_requests = Counter('total_service_requests', 'Total service requests counter')
service_endpoints = ('/metrics', '/_health')


@app.middleware("http")
@REQUEST_TIME.time()
async def log_requests(request: Request, call_next):
    if request.url.path in service_endpoints:
        total_service_requests.inc()
        response = await call_next(request)
    else:
        total_requests.inc()
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
    Instrumentator().instrument(app).expose(app)
    init_tracer()


@app.on_event("shutdown")
async def shutdown():
    logger.info("Disconnected to base")
    mongoengine.disconnect(alias=DB_NAME)


@app.get('/_health')
async def health_check():
    return {
        'status': 'Ok'
    }


app.include_router(router, prefix='/v1')
