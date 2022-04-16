# coding=utf-8

import os
import json
from os.path import dirname, realpath, join, isfile, splitext


class _TextStore():
    def __init__(self):

        self.__defaults: dict[str, str] = {}
        self.__languages: dict[str, dict[str, str]] = {}

        cwd = dirname(realpath(__file__))
        for fname in os.listdir(cwd):
            name, ext = splitext(fname)
            if not ext or ext != ".json":
                continue

            fullp = join(cwd, fname)
            if not isfile(fullp):
                continue

            lang = None
            fields = name.split('.')
            if len(fields) > 1:
                name = fields[0]
                lang = fields[1].lower()

            with open(fullp, "r", encoding="utf-8") as f:
                data = json.loads(f.read())
                if not lang:
                    self.__defaults.update({name+'.'+k: v for k, v in data.items()})

                else:
                    texts = self.__languages.get(lang)
                    if not texts:
                        texts = {}
                        self.__languages[lang] = texts

                    texts.update({name+'.'+k: v for k, v in data.items()})

    def get(self, key: str, lang: str, defval: str) -> str:
        value: str = None
        if lang:
            value = self.__languages.get(lang.lower(), {}).get(key)

        return value or self.__defaults.get(key, defval)


_text_store = _TextStore()


def T(key: str, lang: str = None) -> str:
    return _text_store.get(key, lang, key)


if __name__ == '__main__':
    pass
