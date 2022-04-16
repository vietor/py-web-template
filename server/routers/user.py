# coding=utf-8

from fastapi import APIRouter, Depends

from texts import T
from core.exceptions import (
    InputException
)
from core.db import (
    Session,
    get_session,
    BaseSchema
)
from core.models import (
    MyUserModel,
    MyUserOutSchema
)
from server import auth

router = APIRouter()


class UserLoginInSchema(BaseSchema):
    username: str
    password: str


class UserLoginOutSchema(BaseSchema):
    token: str


@router.post("/login", response_model=UserLoginOutSchema)
def user_login(
        body: UserLoginInSchema,
        session: Session = Depends(get_session)
) -> dict:
    user, token = auth.authenticate_user(body.username.strip().lower(), body.password.strip(), session)

    return {
        'token': token
    }


class UserDetailOutSchema(BaseSchema):
    user: MyUserOutSchema


@router.get("/me", response_model=UserDetailOutSchema)
def user_detail(
        session: Session = Depends(get_session),
        user: MyUserModel = Depends(auth.get_user)
) -> dict:
    return {
        'user': user
    }


class UserUpdatePasswordInSchema(BaseSchema):
    old_password: str
    new_password: str


@router.post("/update/password", response_model=dict)
def user_update_password(
        body: UserUpdatePasswordInSchema,
        session: Session = Depends(get_session),
        user: MyUserModel = Depends(auth.get_user)
) -> dict:
    if user.password != MyUserModel.hash_password(body.old_password.strip()):
        raise InputException(T("user.bad_passwd"))

    user.password = MyUserModel.hash_password(body.new_password.strip())
    session.add(user)
    session.commit()
    return {
        'ok': 1
    }
