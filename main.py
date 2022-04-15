#App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivy.app import App
from kivy.properties import (ObjectProperty)


# Screens
from src.screens.inicio import InicioScreen
from src.screens.modo_juego import ModoJuegoScreen
from src.screens.salvaPantallas import SalvaPantalla


# Configuración Local de la Aplicación
from kivy.config import Config

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

KIVY_CONFIG = str(BASE_DIR.joinpath('miaby.ini'))

IMG_PATH = BASE_DIR.joinpath('resources', 'img')

Config.read(KIVY_CONFIG)


class MIABYApp(App):
    words = {}  # Conjunto de palabras según el idioma
    sm = ScreenManager()  # Manejador de Pantallas
    current_option = "español"  # Opción de la pantalla acutal
    menu_settings_state = True # Estado del Menú de Configuraciones

    inicio_screen = ObjectProperty(None)
    modo_juego_screen = ObjectProperty(None)

    def __init__(self, **kwargs):

        # Definir la escucha del teclado
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self.sm, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        super().__init__(**kwargs)

    def build_config(self, config):
        """
        Construir un archivo de configuraciones local .ini de la aplicación.

        """
        config.setdefaults('kivy', {
            'default_font': "['Roboto', 'data/fonts/Roboto-Regular.ttf', 'data/fonts/Roboto-Italic.ttf', 'data/fonts/Roboto-Bold.ttf', 'data/fonts/Roboto-BoldItalic.ttf']",
            'log_dir': 'logs',
            'log_enable': 1,
            'log_level': 'info',
            'log_name': "kivy_%y-%m-%d_%_.txt"
        })
        config.setdefaults('graphics', {
            'borderless': 1,
            'windows_state': 'visible',
            'fullscreen': 'auto',
            'maxfps': 60,
            'show_cursor': 0,
            'resizable': 1,
        })

    def build(self):
        """
           Construcción de interfaces
            - Inicio
            - Modo de Juego
            - Modo - Observar
            - Modo - Aprender
            - Modo - Practicar
        """
        self. inicio_screen = InicioScreen(name='inicio')
        self. modo_juego_screen = ModoJuegoScreen(name='modo_juego')
        self.sm.add_widget(self.inicio_screen)
        self.sm.add_widget(self.modo_juego_screen)
        # self.sm.add_widget(SalvaPantalla(name='salvaPantallas'))

        self.sm.current = 'inicio'  # Pantalla inicial
        return self.sm

    def get_path_resources(self, tipo, file):
        """
        Generar el path completo de los recursos para cada S.O.
        """
        if tipo == "words":
            return str(BASE_DIR.joinpath("resources","words",file))
        else:
            return str(IMG_PATH.joinpath(tipo, file))

    def manage_screens(self, key):
        """
        Gestionar el comportamiento de la interfaz.
        """
        current_screen = self.sm.current_screen.name
        if key == "up" or key == "down":# Cambiar la opcion de la pantalla actual
            if current_screen == "inicio":
                if self.current_option == "español":
                    self.current_option = "ingles"
                    self.inicio_screen.update_image_buttons_languaje(
                        self.current_option)
                else:
                    self.current_option = "español"
                    self.inicio_screen.update_image_buttons_languaje(
                        self.current_option)
        elif key == "enter":
            if current_screen == "inicio":
                self.inicio_screen.choose_language(lang=self.current_option)


    def _keyboard_closed(self):
        """
        Llamada cuando el teclado se cierra utilizando la tecla escape.
        """
        self.stop()

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        """
        Determinar la tecla presionada y solicitar cambios en la interfaz.
        """
        if keycode[1] == 'escape':
            keyboard.release()
        elif keycode[1] == "f1":
            if self.menu_settings_state:
                self.open_settings()
                self.menu_settings_state = False
            else:
                self.close_settings()
                self.menu_settings_state = True
        else:
            self.manage_screens(keycode[1])
        return True


if __name__ == '__main__':
    MIABYApp().run()
