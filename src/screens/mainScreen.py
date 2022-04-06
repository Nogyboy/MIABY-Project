"""
 docstring
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from src.settings import PATH_IMAGENES

# from playsound import playsound

Builder.load_file('src/screens/mainScreen.kv')


class MainScreen(Screen):
    logo_col = str(PATH_IMAGENES / 'logo.png')
    ojos = str(PATH_IMAGENES / 'imagenojos.png')
