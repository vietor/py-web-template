# coding=utf-8

import os
from pathlib import Path
from os.path import dirname, realpath, abspath


class Config:
    def __init__(self):
        self.LOCAL_DIR = abspath(dirname(dirname(realpath(__file__))))

        ### Basic ###

        self.DISABLE_DOCS = os.environ.get('DISABLE_DOCS', '0') == '1'

        self.JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', "HS256")
        self.JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'ThisAUnsafeSecretKey')
        self.JWT_TOKEN_EXPIRE_DAYS = int(os.environ.get('JWT_EXPIRE_DAYS', '30'))

        self.DATABASE_URL = os.environ.get('DATABASE_URL')

        ### Others ###

        # selt.OTHE_ENV = os.environ.get('OTHER_ENV')

    def local_dir(self, *args) -> str:
        target_dir = os.path.join(self.LOCAL_DIR, *args)
        Path(target_dir).mkdir(exist_ok=True, parents=True)
        return target_dir

    def local_file(self, *args) -> str:
        target_file = os.path.join(self.LOCAL_DIR, *args)
        target_dir = dirname(target_file)
        Path(target_dir).mkdir(exist_ok=True, parents=True)
        return target_file


conf = Config()
