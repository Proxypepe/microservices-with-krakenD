from fastapi import FastAPI
from auth.router import router

app = FastAPI(
    title='Ecommerce API',
    version='0.0.1'
)

app.include_router(router, prefix='/v1')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", reload=True)
