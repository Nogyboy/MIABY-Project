from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from src.settings import PATH_IMAGENES
from src.settings.local import langs

Builder.load_file('src/screens/modo_juego.kv')


class ModoJuegoScreen(Screen):

    def get_data(self):
        return langs.read_json()
