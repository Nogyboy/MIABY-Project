# Configuración Local de la Aplicación
from kivy.config import Config

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

KIVY_CONFIG_PATH = str(BASE_DIR.joinpath('miaby.ini'))

IMG_PATH = BASE_DIR.joinpath('resources', 'img')

AUDIO_PATH = BASE_DIR.joinpath('resources', 'audios')

Config.read(KIVY_CONFIG_PATH)


# Screen
from src.screens.modo_juego import ModoJuegoScreen
from src.screens.inicio import InicioScreen
from src.screens.lectura_tarjeta import LecturaTarjetaScreen
from src.screens.ingresar_texto import IngresarTextoScreen
from src.screens.mensaje import MensajeScreen


# App
from kivy.core.window import Window
from kivy.properties import (ObjectProperty)
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock
from kivy.core.audio import SoundLoader


class MIABYApp(App):

    words = {}  # Conjunto de palabras según el idioma
    sm = ScreenManager()  # Manejador de pantallas
    inicio_option = "español"  # Opción de la pantalla Inicio
    current_option_mode = "observar"  # Opción actual del modo de juego
    modo_option = ("observar", "aprender", "interactuar")
    menu_settings_state = True  # Estado del Menú de Configuraciones
    word_selected = "" # Palabra seleccionada según el idioma
    audio_file = None

    inicio_screen = ObjectProperty(None)
    modo_juego_screen = ObjectProperty(None)
    lectura_tarjeta_screen = ObjectProperty(None)
    ingresar_texto_screen = ObjectProperty(None)
    mensaje_screen = ObjectProperty(None)
    
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
        self.inicio_screen = InicioScreen(name='inicio')
        self.modo_juego_screen = ModoJuegoScreen(name='modo_juego')
        self.lectura_tarjeta_screen = LecturaTarjetaScreen(name="lectura_tarjeta")
        self.ingresar_texto_screen = IngresarTextoScreen(name="ingresar_texto")
        self.mensaje_screen = MensajeScreen(name="mensaje")

        self.sm.add_widget(self.inicio_screen)
        self.sm.add_widget(self.modo_juego_screen)
        self.sm.add_widget(self.lectura_tarjeta_screen)
        self.sm.add_widget(self.ingresar_texto_screen)
        self.sm.add_widget(self.mensaje_screen)
        # self.sm.add_widget(SalvaPantalla(name='salvaPantallas'))
        self.sm.current = "inicio"  # Pantalla inicial
        return self.sm

    def get_path_resources(self, tipo, file, audio_lang: str="español"):
        """
        Generar el path completo de los recursos para cada S.O.
        """
        if tipo == "words":
            return str(BASE_DIR.joinpath("resources", "words", file))
        elif tipo == "audio":
            return str(AUDIO_PATH.joinpath(audio_lang, file))
        else:
            return str(IMG_PATH.joinpath(tipo, file))

    def manage_screens(self, key):
        """
        Gestionar el comportamiento de la interfaz.
        """
        current_screen = self.sm.current_screen.name
        if key == "up" or key == "down":  # Cambiar la opcion de la pantalla de inicio y modo de juego
            if current_screen == "inicio":
                if self.inicio_option == "español":
                    self.inicio_option = "ingles"
                    self.inicio_screen.update_image_buttons_language(
                        self.inicio_option)
                else:
                    self.inicio_option = "español"
                    self.inicio_screen.update_image_buttons_language(
                        self.inicio_option)
            if current_screen == "modo_juego":
                if key == "up":                    
                    pos = self.modo_option.index(self.current_option_mode)-1
                    self.current_option_mode = self.modo_option[2] if pos < 0 else self.modo_option[pos]
                elif key == "down":
                    pos = self.modo_option.index(self.current_option_mode)+1
                    self.current_option_mode = self.modo_option[0] if pos > 2 else self.modo_option[pos]
                
                self.modo_juego_screen.update_image_buttons_mode(
                    self.current_option_mode, self.inicio_option)

        elif key == "enter":# Seleccionar el idioma y modo de juego
            if current_screen == "inicio":
                self.inicio_screen.choose_language(lang=self.inicio_option)
                self.modo_juego_screen.update_image_buttons_mode(
                    self.current_option_mode, self.inicio_option)
                self.lectura_tarjeta_screen.update_background_image(self.inicio_option)
                self.ingresar_texto_screen.update_background_image(self.inicio_option)
                self.mensaje_screen.update_gif(self.inicio_option)
                self.sm.current = "modo_juego"                

            elif current_screen == "modo_juego":
                if self.current_option_mode == "observar":

                    pass
                elif self.current_option_mode == "aprender":
                    pass

                elif self.current_option_mode == "interactuar":
                    self.sm.current = "lectura_tarjeta"

            elif current_screen == "lectura_tarjeta":
                self.sm.current = "ingresar_texto"

        elif key == "left":# Botón de regresar
            if current_screen == "modo_juego":
                self.sm.current = "inicio"
            elif current_screen == "lectura_tarjeta":
                self.sm.current = "modo_juego"
            elif current_screen == "ingresar_texto":
                self.sm.current = "lectura_tarjeta"
        else:
            if current_screen == "ingresar_texto":
                self.ingresar_texto_screen.validate_word_entry(key.upper())

    def load_audio(self, file, lang):
        """
        Cargar audio
        """
        self.audio_file = SoundLoader.load(self.get_path_resources("audio", file, audio_lang=lang))
        

    def play_audio(self):
        """
        Reproducir audio
        """
        if self.audio_file:
            self.audio_file.play()

    def stop_audio(self):
        """
        Detener audio
        """
        if self.audio_file:
            self.audio_file.stop()
            self.audio_file.unload()

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
