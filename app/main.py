import uvicorn
from fastapi import Depends, FastAPI
from app.endpoints import shop_unit_type, imports
from app.db.base import database

app = FastAPI(
    title="FastAPI",
    version="0.1.0"
)
app.include_router(shop_unit_type.router, prefix='/shop_unit_type', tags=["shop_unit_type"])
app.include_router(imports.router, prefix='/imports', tags=["imports"])


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
