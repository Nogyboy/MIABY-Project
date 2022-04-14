"""
 docstring
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App

from src.settings import PATH_IMAGENES
# from playsound import playsound

Builder.load_file('src/screens/inicio.kv')


class InicioScreen(Screen):
    
    def seleccionar_idioma(self, lang: str = 'es'):
        """
        Selección de idioma, se almacena en la variable idioma de la clase
        MIABYApp.
        """
        app = App.get_running_app()
        app.idioma = lang
        del app
