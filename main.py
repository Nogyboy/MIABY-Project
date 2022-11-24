from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivy.app import App
from kivy.properties import (ObjectProperty)
from kivy.core.window import Window
from src.screens.screensaver import ScreenSaverScreen
from src.screens.welcome import WelcomeScreen
from src.screens.show_video import ShowVideoScreen
from src.screens.message import MessageScreen
from src.screens.text_input import TextInputScreen
from src.screens.read_card import ReadCardScreen
from src.screens.home import HomeScreen
from src.screens.game_mode import GameModeScreen
import time
from kivy.config import Config
from pathlib import Path

# BASE DIRECTORY
BASE_DIR = Path(__file__).resolve().parent

# Load app's configuration
KIVY_CONFIG_PATH = str(BASE_DIR.joinpath('miaby.ini'))
Config.read(KIVY_CONFIG_PATH)


class MIABYApp(App):

    menu_settings_state = True  # State of kivy menu built-in
    sm = ScreenManager()

    modo_option = ("observe", "learning", "interact")
    words = {}  # Words selected base on language
    word_selected = ""

    lang_option = "spanish"
    option_game_mode = "observe"

    audio_file = None

    # Screens variables
    welcome_screen = ObjectProperty(None)
    home_screen = ObjectProperty(None)
    game_mode_screen = ObjectProperty(None)
    read_card_screen = ObjectProperty(None)
    text_input_screen = ObjectProperty(None)
    message_screen = ObjectProperty(None)
    show_video_screen = ObjectProperty(None)
    screensaver_screen = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.config.get('extras', 'mode_app') == "board":
            self.gpio_set_up()
            Clock.schedule_interval(self.read_keyboard, 0.25)
        else:
            self._keyboard = Window.request_keyboard(
                self._keyboard_closed, self.sm, 'text')
            self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def build(self):
        """
           Build screens
            - Home
            - Game Mode
            - Mode - Observe
            - Mode - Learning
            - Mode - Interact
        """

        self.welcome_screen = WelcomeScreen(name="welcome")
        self.home_screen = HomeScreen(name='home')
        self.game_mode_screen = GameModeScreen(name='game_mode')
        self.read_card_screen = ReadCardScreen(name="read_card")
        self.text_input_screen = TextInputScreen(name="text_input")
        self.message_screen = MessageScreen(name="message")
        self.show_video_screen = ShowVideoScreen(name="show_video")
        self.screensaver_screen = ScreenSaverScreen(name="inactivity")

        self.sm.add_widget(self.welcome_screen)
        self.sm.add_widget(self.home_screen)
        self.sm.add_widget(self.game_mode_screen)
        self.sm.add_widget(self.read_card_screen)
        self.sm.add_widget(self.text_input_screen)
        self.sm.add_widget(self.message_screen)
        self.sm.add_widget(self.show_video_screen)
        self.sm.add_widget(self.screensaver_screen)

        self.sm.current = "welcome"  # First screen
        return self.sm

    def gpio_set_up(self):
        """
        Set up each GPIO of Raspberry Pi BOARD in case mode_app == "desktop".
        """
        import RPi.GPIO as GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        rows = [19, 26, 13, 6]
        columns = [17, 27, 22, 1, 12, 16, 20, 23]

        for row in rows:
            GPIO.setup(row, GPIO.OUT)

        for j in range(8):
            GPIO.setup(columns[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def get_path_resources(self, res_type, file):
        """
        Get paths for resources.
        """
        paths = {
            "words": str(BASE_DIR.joinpath("resources", "words", file)),
            "audio": str(BASE_DIR.joinpath('resources', 'audios').joinpath(self.lang_option, file)),
            "video": str(BASE_DIR.joinpath('resources', 'video').joinpath(self.option_game_mode, self.lang_option, file)),
            "images": str(BASE_DIR.joinpath('resources', 'img').joinpath(self.lang_option, file))
        }

        return paths[res_type]

    def manage_screens(self, key):
        """
        Manage app behavior.
        """
        current_screen = self.sm.current_screen.name
        if key == "up" or key == "down":
            if current_screen == "home":
                self.home_screen.update_image_buttons_language(
                    "english" if self.lang_option == "spanish" else "spanish")

            elif current_screen == "game_mode":
                if key == "up":
                    pos = self.modo_option.index(self.option_game_mode)-1
                    # @TODO Use negative indexes
                    self.option_game_mode = self.modo_option[2] if pos < 0 else self.modo_option[pos]
                elif key == "down":
                    # @TODO Refactor with an if on 2 index
                    pos = self.modo_option.index(self.option_game_mode)+1
                    self.option_game_mode = self.modo_option[0] if pos > 2 else self.modo_option[pos]

                self.game_mode_screen.update_image_buttons_mode(
                    self.option_game_mode, self.lang_option)

        elif key == "enter":  # Seleccionar el idioma y modo de juego
            if current_screen == "bienvenida":
                self.sm.current = "inicio"

            elif current_screen == "inicio":
                self.home_screen.choose_language(lang=self.lang_option)
                self.game_mode_screen.update_image_buttons_mode(
                    self.option_game_mode, self.lang_option)
                self.read_card_screen.update_background_image(self.lang_option)
                self.text_input_screen.update_background_image(
                    self.lang_option)
                self.message_screen.update_gif(self.lang_option)
                self.sm.current = "modo_juego"

            elif current_screen == "modo_juego":
                if self.option_game_mode == "observar":
                    self.show_video_screen.select_random_video()
                    self.stop_audio()
                    self.load_audio("5.wav", bind=True)
                    self.play_audio()
                elif self.option_game_mode == "aprender":
                    self.show_video_screen.select_random_video()
                    self.stop_audio()
                    self.load_audio("4.wav", bind=True)
                    self.play_audio()

                elif self.option_game_mode == "interactuar":
                    self.stop_audio()
                    self.load_audio("6.wav", bind=True)
                    self.play_audio()

            elif current_screen == "video":
                self.show_video_screen.video.state = "play"
            elif current_screen == "inactividad":
                self.sm.current = "inicio"

        elif key == "left":  # Botón de regresar
            if current_screen == "modo_juego":
                self.sm.current = "inicio"
            elif current_screen == "lectura_tarjeta":
                try:
                    self.read_card_screen.event.cancel()
                except AttributeError:
                    print("Muy rápido la instacia no se crea.")
                self.sm.current = "modo_juego"
            elif current_screen == "ingresar_texto":
                self.sm.current = "lectura_tarjeta"
            elif current_screen == "video":
                self.sm.current = "modo_juego"
        elif key == "right":
            if current_screen == "video":
                self.show_video_screen.video.state = "pause"
        else:
            if current_screen == "text_input":
                self.text_input_screen.validate_word_entry(key.upper())

    def load_audio(self, file, bind: bool = False):
        """
        Cargar audio
        """
        if KEYBOARD_MODE:
            self.audio_file = SoundLoader.load(
                self.get_path_resources("audio", file))
            if bind:
                self.audio_file.bind(on_stop=self.do_after_stop_audio)
            else:
                self.audio_file.unbind()

    def play_audio(self):
        """
        Reproducir audio
        """
        if KEYBOARD_MODE:
            if self.audio_file:
                self.audio_file.play()

    def stop_audio(self):
        """
        Detener audio
        """
        try:
            if KEYBOARD_MODE:
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
            if self.option_game_mode == "observar" or self.option_game_mode == "aprender":
                self.sm.current = "video"
                self.audio_file.unload()
            elif self.option_game_mode == "interactuar":
                self.sm.current = "lectura_tarjeta"
                self.audio_file.unload()

    def read_coordinate(self, fila, caracteres):
        """
        Lectura de la coordenada según la fila leída.
        """
        GPIO.output(fila, GPIO.HIGH)
        coordenada = 0
        for pin in Columnas:
            if bool(GPIO.input(pin)):
                self.manage_screens(key=caracteres[coordenada])
                time.sleep(0.3)
            coordenada += 1
        GPIO.output(fila, GPIO.LOW)

    def read_keyboard(self, *args):
        key_map = (
            ("A", "B", "C", "D", "E", "F", "G", "up"),
            ("H", "I", "J", "K", "L", "M", "N", "down"),
            ("O", "P", "Q", "R", "S", "T", "Ñ", "enter"),
            ("left", "U", "V", "W", "X", "Y", "Z", "right")
        )
        arrow_keys = 0
        for fila in Filas:
            self.read_coordinate(fila, key_map[arrow_keys])
            arrow_keys += 1

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
