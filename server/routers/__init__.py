# coding=utf-8

from fastapi import APIRouter
from server.routers import (
    user,
)

api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["User"])
