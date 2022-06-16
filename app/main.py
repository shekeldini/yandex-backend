import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.endpoints import imports, nodes, delete, sales
from app.db.base import database
from app.models.Error import Error

from fastapi.exceptions import RequestValidationError, ValidationError, HTTPException
from app.core.utils import TooManyRequests, remove_422_from_app

app = FastAPI(
    title="Mega Market Open API",
    version="1.0",
    description="Вступительное задание в Летнюю Школу Бэкенд Разработки Яндекса 2022"
)

app.include_router(imports.router, prefix='/imports', tags=["Базовые задачи"])
app.include_router(nodes.router, prefix='/nodes', tags=["Базовые задачи"])
app.include_router(delete.router, prefix='/delete', tags=["Базовые задачи"])
app.include_router(sales.router, prefix='/sales', tags=["Дополнительные задачи"])
remove_422_from_app(app)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(Error(code=400, message="Validation Failed").dict(), status_code=400)


@app.exception_handler(HTTPException)
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


@app.get("/")
async def read_root():
    return {"hello": "world"}


if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost', reload=False)
