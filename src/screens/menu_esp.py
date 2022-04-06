from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from src.settings import PATH_IMAGENES
from src.settings.local import langs

Builder.load_file('src/screens/pantalla2.kv')


class MenuEsp(Screen):
    # name: str = 'menu_esp'
    logo_colegio: str = str(PATH_IMAGENES / 'logo.png')
    ojos: str = str(PATH_IMAGENES / 'logo.png')

    def get_data(self):
        return langs.read_json()
