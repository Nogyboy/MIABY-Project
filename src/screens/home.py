from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import (ObjectProperty)
from kivy.clock import Clock

import json


Builder.load_file('src/screens/home.kv')


class HomeScreen(Screen):

    esp_button = ObjectProperty(None)
    en_button = ObjectProperty(None)
    event = None
    secs = 0
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()


    def choose_language(self, lang):
        """
        Load words from JSON File.
        """
        path_json_words = self.app.get_path_resources("words","data.json")

        with open(path_json_words, encoding="utf-8") as file:
            self.app.words = json.load(file)[lang]

    def update_image_buttons_language(self, option):
        """
        Update image button base on its state.
        """
        if option == "spanish":
            self.esp_button.source = self.app.get_path_resources("button_esp_down.png")
            self.en_button.source = self.app.get_path_resources("button_ingles_normal.png")
        elif option == "english":
            self.esp_button.source = self.app.get_path_resources("button_esp_normal.png")
            self.en_button.source = self.app.get_path_resources("button_ingles_down.png")

        self.esp_button.reload()
        self.en_button.reload()

    def update_time(self, sec):
        """
        Contador de tiempo de visualización del mensaje.
        """
        self.secs = self.secs+1
        if self.secs == 120:
            self.event.cancel()
            self.secs = 0
            self.app.sm.current = "inactividad"

    def on_enter(self, *args):
        try:
            self.app.load_audio("1.wav")
            self.app.play_audio()
        except AttributeError:
            self.on_enter()
        self.event = Clock.schedule_interval(self.update_time, 1)
        return super().on_enter(*args)
    
    def on_pre_leave(self, *args):
        try:
            self.event.cancel()
        except AttributeError:
            print("Instancia no creada...")
        if self.app.audio_file:
            self.app.stop_audio()
        return super().on_pre_leave(*args)
