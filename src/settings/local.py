import json

from src.settings import PATH_LANG


class Local:
    lang_accept = ['es', 'en']
    default_lang = 'es'
    path: str = ''

    def __init__(self, lang=None):

        if lang is None:
            self.lang = self.default_lang
        else:
            assert (lang in self.lang_accept)
            self.lang = lang
        print(f'Defaulf Language: {self.lang}')


    def equals(self, lang: str) -> bool:
        print(f'{lang}=={self.lang} -> {lang == self.lang}')
        return lang == self.lang

    def get_lang(self) -> str:
        return self.lang

    def set_lang(self, new_lang) -> None:
        assert (new_lang in self.lang_accept)
        self.lang = new_lang
        print(f'Set lang {self.lang} to {new_lang}')

    def read_json(self) -> dict:

        if self.lang == 'es':
            self.path = str(PATH_LANG / 'esp' / 'esp.json')
        else:
            self.path = str(PATH_LANG / 'eng' / 'eng.json')

        print(f'Path Json Lang {self.path}')

        with open(self.path) as file:
            data = json.load(file)

            return data


langs = Local()
