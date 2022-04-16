# coding=utf-8

from typing import Tuple
from datetime import datetime, timedelta

from jose import jwt
from fastapi import Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from texts import T
from core.config import conf
from core.exceptions import (
    TokenException,
    InputException
)
from core.db import (
    Session,
    get_session
)
from core.models import MyUserModel


class JWTBearer(HTTPBearer):
    def __init__(self):
        super(JWTBearer, self).__init__(auto_error=False)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if not credentials or not credentials.scheme == "Bearer":
            raise TokenException()

        try:
            return jwt.decode(credentials.credentials, conf.JWT_SECRET_KEY, algorithms=[conf.JWT_ALGORITHM])
        except Exception:
            raise TokenException()


def get_user(data: dict = Depends(JWTBearer()), session: Session = Depends(get_session)) -> MyUserModel:
    user = session.query(MyUserModel).filter_by(id=data['uid']).first()
    if not user or user.status < 0:
        raise TokenException(T("user.not_found_or_blocked"))

    return user


def authenticate_user(username: str, password: str, session: Session) -> Tuple[MyUserModel, str]:
    user = session.query(MyUserModel).filter_by(username=username).first()
    if not user or user.password != MyUserModel.hash_password(password):
        raise InputException(T("user.not_found_or_bad_passwd"))

    if user.status < 0:
        raise InputException(T("user.blocked"))

    data = {
        'uid': user.id,
        'exp': datetime.utcnow() + timedelta(days=conf.JWT_TOKEN_EXPIRE_DAYS)
    }
    return user, jwt.encode(data, conf.JWT_SECRET_KEY, algorithm=conf.JWT_ALGORITHM)
