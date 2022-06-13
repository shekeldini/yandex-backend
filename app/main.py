import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.endpoints import shop_unit_type, imports, nodes, delete
from app.db.base import database, redis
from app.models.Error import Error

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from redis_rate_limit import TooManyRequests

app = FastAPI(
    title="FastAPI",
    version="0.1.0"
)
app.include_router(shop_unit_type.router, prefix='/shop_unit_type', tags=["shop_unit_type"])
app.include_router(imports.router, prefix='/imports', tags=["imports"])
app.include_router(nodes.router, prefix='/nodes', tags=["nodes"])
app.include_router(delete.router, prefix='/delete', tags=["delete"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(Error(code=400, message="Validation Failed").dict(), status_code=400)


@app.exception_handler(StarletteHTTPException)
async def validation_exception_handler(request, exc):
    return JSONResponse(Error(code=404, message="Item not found").dict(), status_code=exc.status_code)


@app.exception_handler(TooManyRequests)
async def validation_exception_handler(request, exc):
    return JSONResponse(Error(code=429, message="Too many requests").dict(), status_code=429)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    redis.close()


@app.get("/")
async def read_root():
    return {"hello": "world"}


if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost', reload=False)
