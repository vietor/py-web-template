# coding=utf-8

from fastapi.exceptions import HTTPException


class InputException(HTTPException):
    def __init__(self, message: str):
        super(HTTPException, self).__init__(status_code=400, detail=message)


class TokenException(HTTPException):
    def __init__(self, message: str = None):
        super(HTTPException, self).__init__(status_code=403, detail=message or 'Not authenticated')
