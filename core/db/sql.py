# coding=utf-8

from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from core.config import conf


if conf.DATABASE_URL:
    engine = create_engine(conf.DATABASE_URL)

else:
    sqlite_file = conf.local_file("data", "main.sqlite")
    engine = create_engine(f"sqlite:///{sqlite_file}", connect_args={
        "check_same_thread": False
    })

DBase = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


class SessionContext(object):
    def __init__(self):
        self.session = SessionLocal()

    def __enter__(self) -> Session:
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
