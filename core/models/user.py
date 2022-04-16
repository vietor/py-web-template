# coding=utf-8

import hashlib
from typing import Optional

from core.db import BaseDBModel, BaseDateSchema

from sqlalchemy import (
    Column,
    Integer,
    SmallInteger,
    VARCHAR,
)


class MyUserModel(BaseDBModel):

    __tablename__ = "my_users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    username = Column(VARCHAR(128), index=True, unique=True, nullable=False)
    password = Column(VARCHAR(256), nullable=False)

    display_name = Column(VARCHAR(128), index=True, nullable=False)
    avatar_url = Column(VARCHAR(1024))

    status = Column(SmallInteger, default=0, nullable=False, doc="0-normal, -1-blocked")

    @classmethod
    def hash_password(cls, password: str) -> str:
        text = 'PASSWORD:' + password
        return hashlib.sha1(text.encode('utf-8')).hexdigest()


class MyUserOutSchema(BaseDateSchema):
    id: int
    status: int
    username: str
    display_name: str
    avatar_url: Optional[str]
