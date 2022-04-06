"""
 docstring
"""
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

from src.settings import PATH_IMAGENES
# from playsound import playsound

Builder.load_file('src/screens/mainScreen.kv')


class MainScreen(MDScreen):
    logo_col = str(PATH_IMAGENES / 'logo.png')
    ojos = str(PATH_IMAGENES / 'imagenojos.png')



