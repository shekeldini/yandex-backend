import uvicorn
from fastapi import Depends, FastAPI

from app.db.base import database

app = FastAPI(
    title="FastAPI",
    version="0.1.0"
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def read_root():
    return {"hello": "world"}


if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost', reload=False)
