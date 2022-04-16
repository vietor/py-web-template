# coding=utf-8

import json
from typing import Type, TypeVar
from datetime import datetime, date

from pydantic import BaseModel
from sqlalchemy import func, Column, DateTime
from sqlalchemy.schema import CreateTable
from sqlalchemy.ext.compiler import compiles

from core.db.sql import DBase, Session


T = TypeVar("T")


class BaseEncoder(json.JSONEncoder):
    @classmethod
    def encode_date(cls, o: date) -> str:
        return o.strftime('%Y-%m-%d')

    @classmethod
    def encode_datetime(cls, o: datetime) -> str:
        return o.strftime('%Y-%m-%d %H:%M:%S')

    def default(self, o):
        if isinstance(o, date):
            return self.encode_date(o)

        elif isinstance(o, datetime):
            return self.encode_datetime(o)

        else:
            return json.JSONEncoder.default(self, o)


class BaseDBModel(DBase):
    __abstract__ = True

    RESERVED_COLUMNS = 2
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,  server_default=func.now(), server_onupdate=func.now(), nullable=False)

    def update(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)

    def to_dict(self) -> dict:
        names = [c.name for c in self.__table__.columns]
        return {key: getattr(self, key, None) for key in names}

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, cls=BaseEncoder)

    @classmethod
    def instance(cls: Type[T], session: Session, **kwargs: dict) -> T:
        model = session.query(cls).filter_by(**kwargs).first()
        if not model:
            model = cls(**kwargs)

        return model


@compiles(CreateTable)
def _compile_create_table(element, compiler, **kwargs) -> str:
    reserved = BaseDBModel.RESERVED_COLUMNS
    element.columns = element.columns[reserved:] + element.columns[:reserved]
    return compiler.visit_create_table(element)


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        json_encoders = {
            date: BaseEncoder.encode_date,
            datetime: BaseEncoder.encode_datetime
        }


class BaseDateSchema(BaseSchema):
    created_at: datetime
    updated_at: datetime
