from kivy.config import Config
from pathlib import Path

# BASE DIRECTORY
BASE_DIR = Path(__file__).resolve().parent

# Load app's configuration
KIVY_CONFIG_PATH = str(BASE_DIR.joinpath('miaby.ini'))
Config.read(KIVY_CONFIG_PATH) # To read its own ini file must be first

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


class MIABYApp(App):

    menu_settings_state = True  # State of kivy menu built-in
    sm = ScreenManager()

    modo_option = ("observe", "learning", "interact")
    words = {}  # Words selected base on language
    word_selected = ""

    rows = [19, 26, 13, 6]
    columns = [17, 27, 22, 1, 12, 16, 20, 23]

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
        self.config_mode = None
        super().__init__(**kwargs)
        

    def build_config(self, config):
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
        print(self.get_application_config())
        self.config_mode = self.config.get('extras', 'mode_app')
        self.config.set('graphics', 'fullscreen','auto')
        if self.config_mode == "board":
            self.gpio_set_up()
            Clock.schedule_interval(self.read_keyboard, 0.25)
        else:
            self._keyboard = Window.request_keyboard(
                self._keyboard_closed, self.sm, 'text')
            self._keyboard.bind(on_key_down=self._on_keyboard_down)

        return self.sm
        


    def gpio_set_up(self):
        """
        Set up each GPIO of Raspberry Pi BOARD in case mode_app == "desktop".
        """
        import RPi.GPIO as GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        for row in self.rows:
            GPIO.setup(row, GPIO.OUT)

        for j in range(8):
            GPIO.setup(self.columns[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def get_path_resources(self, res_type, file, lang_opt=""):
        """
        Get paths for resources.
        """
        paths = {
            "words": str(BASE_DIR.joinpath("resources", "words", file)),
            "audio": str(BASE_DIR.joinpath('resources', 'audios').joinpath(self.lang_option, file)),
            "video": str(BASE_DIR.joinpath('resources', 'videos').joinpath(file)),
            "images": str(BASE_DIR.joinpath('resources', 'img').joinpath(self.lang_option, file)),
            "images_config" : str(BASE_DIR.joinpath('resources', 'img').joinpath(lang_opt, file)),
            "common": str(BASE_DIR.joinpath('resources', 'img').joinpath("common", file))
        }

        return paths[res_type]

    def manage_screens(self, key):
        """
        Manage app behavior.
        """
        current_screen = self.sm.current_screen.name
        if key == "up" or key == "down":
            if current_screen == "home":
                self.lang_option = "english" if self.lang_option == "spanish" else "spanish"
                self.home_screen.update_image_buttons_language(
                    self.lang_option)

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

        elif key == "enter":
            if current_screen == "welcome":
                self.sm.current = "home"

            elif current_screen == "home":
                self.home_screen.choose_language(lang=self.lang_option)

                self.game_mode_screen.update_image_buttons_mode(
                    self.option_game_mode, self.lang_option)
                self.read_card_screen.update_background_image(self.lang_option)
                self.text_input_screen.update_background_image(
                    self.lang_option)
                self.message_screen.update_image(self.lang_option)

                self.sm.current = "game_mode"

            elif current_screen == "game_mode":
                if self.option_game_mode == "observe":
                    self.show_video_screen.select_random_video()
                    self.stop_audio()
                    self.load_audio("1.wav", bind=True)
                    self.play_audio()

                elif self.option_game_mode == "learning":
                    self.show_video_screen.select_random_video()
                    self.stop_audio()
                    self.load_audio("1.wav", bind=True)
                    self.play_audio()

                elif self.option_game_mode == "interact":
                    self.stop_audio()
                    self.load_audio("1.wav", bind=True)
                    self.play_audio()

            elif current_screen == "show_video":
                self.show_video_screen.video.state = "play"

            elif current_screen == "inactivity":
                self.sm.current = "home"

        elif key == "left":
            if current_screen == "game_mode":
                self.sm.current = "home"
            elif current_screen == "read_card" and self.config_mode == "board":
                try:
                    self.read_card_screen.event.cancel()
                except AttributeError:
                    print("Too fast the screen hasn't created.")
                self.sm.current = "game_mode"
            elif current_screen == "text_input":
                self.sm.current = "read_card"
            elif current_screen == "show_video":
                self.sm.current = "game_mode"

        elif key == "right":
            if current_screen == "video":
                self.show_video_screen.video.state = "pause"
        else:
            if current_screen == "text_input":
                self.text_input_screen.validate_word_entry(key.upper())

    # ------------- Audio ---------------------
    def load_audio(self, file, bind: bool = False):
        """
        Load audio
        """
        self.audio_file = SoundLoader.load(
            self.get_path_resources("audio", file))
        if bind:
            self.audio_file.bind(on_stop=self.do_after_stop_audio)
        else:
            self.audio_file.unbind()

    def play_audio(self):
        """
        Play audio
        """
        if self.audio_file:
            self.audio_file.play()

    def stop_audio(self):
        """
        Stop audio
        """
        try:
            if self.audio_file:
                self.audio_file.stop()
                self.audio_file.unload()
        except AttributeError:
            print("File not loaded.")
        except Exception as e:
            print(f"Exception: {e}")

    def do_after_stop_audio(self, *args):
        """
        Do after audio ends.
        """
        current_screen = self.sm.current_screen.name
        if self.audio_file and current_screen == "game_mode":
            if self.option_game_mode == "observe" or self.option_game_mode == "learning":
                self.sm.current = "video"
                self.audio_file.unload()
            elif self.option_game_mode == "interact":
                self.sm.current = "read_card"
                self.audio_file.unload()

    # ------------- Keyboard ---------------------
    def read_coordinate(self, fila, characters):
        """
        Read character base on rows and columns.
        """
        GPIO.output(fila, GPIO.HIGH)
        coordinate = 0
        for pin in self.columns:
            if bool(GPIO.input(pin)):
                self.manage_screens(key=characters[coordinate])
                time.sleep(0.3)
            coordinate += 1
        GPIO.output(fila, GPIO.LOW)

    def read_keyboard(self, *args):
        key_map = (
            ("A", "B", "C", "D", "E", "F", "G", "up"),
            ("H", "I", "J", "K", "L", "M", "N", "down"),
            ("O", "P", "Q", "R", "S", "T", "Ñ", "enter"),
            ("left", "U", "V", "W", "X", "Y", "Z", "right")
        )
        arrow_keys = 0
        for fila in self.rows:
            self.read_coordinate(fila, key_map[arrow_keys])
            arrow_keys += 1

    def _keyboard_closed(self):
        """
        Called when press Escape key.
        """
        self.stop()

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        """
        Called on every pressed key.
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
