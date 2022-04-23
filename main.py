import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#Definición de lineas y columnas
Filas = [19,26, 13, 6]
Columnas = [17, 27, 22,1 ,12, 16,20,23]

# Inicializar los pines GPIO
for row in Filas:
    GPIO.setup(row, GPIO.OUT)

for j in range(8):
    GPIO.setup(Columnas[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Configuración Local de la Aplicación
from kivy.config import Config

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

KIVY_CONFIG_PATH = str(BASE_DIR.joinpath('miaby.ini'))

IMG_PATH = BASE_DIR.joinpath('resources', 'img')

AUDIO_PATH = BASE_DIR.joinpath('resources', 'audios')

VIDEO_PATH = BASE_DIR.joinpath('resources', 'video')

Config.read(KIVY_CONFIG_PATH)

# Screen
from src.screens.modo_juego import ModoJuegoScreen
from src.screens.inicio import InicioScreen
from src.screens.lectura_tarjeta import LecturaTarjetaScreen
from src.screens.ingresar_texto import IngresarTextoScreen
from src.screens.mensaje import MensajeScreen
from src.screens.mostrar_video import MostrarVideoScreen
from src.screens.bienvenida import BienvenidaScreen
from src.screens.salvapantalla import SalvaPantallaScreen

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
    audio_file = None # Archivo de audio

    bienvenida_screen = ObjectProperty(None)
    inicio_screen = ObjectProperty(None)
    modo_juego_screen = ObjectProperty(None)
    lectura_tarjeta_screen = ObjectProperty(None)
    ingresar_texto_screen = ObjectProperty(None)
    mensaje_screen = ObjectProperty(None)
    video_screen = ObjectProperty(None)
    salvapantalla_screen = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        # Definir la escucha del teclado
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self.sm, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        Clock.schedule_interval(self.read_keayboard, 0.40)
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

        self.bienvenida_screen = BienvenidaScreen(name="bienvenida")
        self.inicio_screen = InicioScreen(name='inicio')
        self.modo_juego_screen = ModoJuegoScreen(name='modo_juego')
        self.lectura_tarjeta_screen = LecturaTarjetaScreen(name="lectura_tarjeta")
        self.ingresar_texto_screen = IngresarTextoScreen(name="ingresar_texto")
        self.mensaje_screen = MensajeScreen(name="mensaje")
        self.video_screen = MostrarVideoScreen(name="video")
        self.salvapantalla_screen = SalvaPantallaScreen(name="inactividad")

        self.sm.add_widget(self.bienvenida_screen)
        self.sm.add_widget(self.inicio_screen)
        self.sm.add_widget(self.modo_juego_screen)
        self.sm.add_widget(self.lectura_tarjeta_screen)
        self.sm.add_widget(self.ingresar_texto_screen)
        self.sm.add_widget(self.mensaje_screen)
        self.sm.add_widget(self.video_screen)
        self.sm.add_widget(self.salvapantalla_screen)

        self.sm.current = "bienvenida"  # Pantalla inicial
        return self.sm

    def get_path_resources(self, tipo, file):
        """
        Generar el path completo de los recursos para cada S.O.
        """
        if tipo == "words":
            return str(BASE_DIR.joinpath("resources", "words", file))

        elif tipo == "audio":
            return str(AUDIO_PATH.joinpath(self.inicio_option, file))

        elif tipo == "video":
            return str(VIDEO_PATH.joinpath(self.current_option_mode, self.inicio_option, file))

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
            if current_screen == "bienvenida":
                self.sm.current = "inicio"

            elif current_screen == "inicio":
                self.inicio_screen.choose_language(lang=self.inicio_option)
                self.modo_juego_screen.update_image_buttons_mode(
                    self.current_option_mode, self.inicio_option)
                self.lectura_tarjeta_screen.update_background_image(self.inicio_option)
                self.ingresar_texto_screen.update_background_image(self.inicio_option)
                self.mensaje_screen.update_gif(self.inicio_option)
                self.sm.current = "modo_juego"
                # self.load_audio("2.wav", bind=True)
                # self.play_audio()               

            elif current_screen == "modo_juego":
                if self.current_option_mode == "observar":
                    self.video_screen.select_random_video()
                    self.stop_audio()
                    self.load_audio("5.wav", bind=True)
                    self.play_audio()
                elif self.current_option_mode == "aprender":
                    self.video_screen.select_random_video()
                    self.stop_audio()
                    self.load_audio("4.wav", bind=True)
                    self.play_audio()
 
                elif self.current_option_mode == "interactuar":
                    self.stop_audio()
                    self.load_audio("6.wav", bind=True)
                    self.play_audio()

            elif current_screen == "video":
                self.video_screen.stop_play_video("play")
            elif current_screen == "inactividad":
                self.sm.current = "inicio"

        elif key == "left":# Botón de regresar
            if current_screen == "modo_juego":
                self.sm.current = "inicio"
            elif current_screen == "lectura_tarjeta":
                self.lectura_tarjeta_screen.event.cancel()
                self.sm.current = "modo_juego"
            elif current_screen == "ingresar_texto":
                self.sm.current = "lectura_tarjeta"
            elif current_screen == "video":
                self.sm.current = "modo_juego"
        elif key == "right":
            if current_screen == "video":
                self.video_screen.stop_play_video("pause")
        else:
            if current_screen == "ingresar_texto":
                self.ingresar_texto_screen.validate_word_entry(key.upper())

    def load_audio(self, file, bind: bool = False):
        """
        Cargar audio
        """
        self.audio_file = SoundLoader.load(self.get_path_resources("audio", file))
        if bind:
            self.audio_file.bind(on_stop=self.do_after_stop_audio)
        else:
            self.audio_file.unbind()
        

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
        try:   
            if self.audio_file:
                self.audio_file.stop()
                self.audio_file.unload()
        except AttributeError:
            print("Audio no cargado.")
        except Exception as e:
            print(f"Excepción no controlada: {e}")

    def do_after_stop_audio(self, *args):
        """
        Realizar una acción despúes de finalizar el audio
        """
        current_screen = self.sm.current_screen.name
        if self.audio_file and current_screen == "modo_juego":
            if self.current_option_mode == "observar" or self.current_option_mode=="aprender":
                self.sm.current = "video"
                self.audio_file.unload()
            elif self.current_option_mode == "interactuar":
                self.sm.current = "lectura_tarjeta"
                self.audio_file.unload()
        # elif self.audio_file and current_screen == "inicio":
        #     self.sm.current = "modo_juego"

    def read_coordinate(self, fila, caracteres):
        """
        Lectura de la coordenada según la fila leída.
        """
        GPIO.output(fila, GPIO.HIGH)  
        coordenada = 0
        for pin in Columnas:
            if bool(GPIO.input(pin)):
                self.manage_screens(key=caracteres[coordenada])
            coordenada+=1
        GPIO.output(fila,GPIO.LOW)

    def read_keayboard(self, *args):
        key_map = (
            ("A", "B", "C", "D", "E", "F", "G", "up"),
        ("H", "I", "J", "K", "L", "M", "N", "down"),
        ("O", "P", "Q", "R", "S", "T", "Ñ", "enter"),
        ("left","U", "V", "W", "X", "Y", "Z", "right")
        )
        arrow_keys = 0
        for fila in Filas:
            self.read_coordinate(fila, key_map[arrow_keys])
            arrow_keys+=1

    def _keyboard_closed(self):
        """
        Llamada cuando el teclado se cierra utilizando la tecla escape
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
