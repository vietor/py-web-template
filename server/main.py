# coding=utf-8

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from sqlalchemy.orm.exc import NoResultFound

from texts import T
from core.config import conf
from server.routers import api_router

app = FastAPI(
    title="Server",
    docs_url=None if conf.DISABLE_DOCS else "/docs"
)

app.include_router(api_router, prefix='/api')

app.mount("/", StaticFiles(directory=conf.local_dir('static'), html=True), name="static")


@app.exception_handler(NoResultFound)
def not_found_handler(request: Request, exc: NoResultFound) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": "Not Found"}
    )


@app.exception_handler(Exception)
def unknow_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": T(str(exc))}
    )


if __name__ == '__main__':
    uvicorn.run(app=app, host="0.0.0.0")
