from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import (ObjectProperty)

import json


Builder.load_file('src/screens/inicio.kv')


class InicioScreen(Screen):

    esp_boton = ObjectProperty(None)
    en_boton = ObjectProperty(None)
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()


    def choose_language(self, lang):
        """
        Selección de idioma, se almacena en la variable idioma de la clase
        MIABYApp.
        """
        path_json_words = self.app.get_path_resources("words","data.json")

        with open(path_json_words, encoding="utf-8") as file:
            self.app.words = json.load(file)[lang]

    def update_image_buttons_language(self, option):
        """
        Actualiza la imagen del botón en función de la
        opción que se encuentre actualmente seleccionada.
        """
        if option == "español":
            self.esp_boton.source = self.app.get_path_resources(
                "español", "boton_esp_down.png")
            self.en_boton.source = self.app.get_path_resources(
                "ingles", "boton_ingles_normal.png")
        elif option == "ingles":
            self.esp_boton.source = self.app.get_path_resources(
                "español", "boton_esp_normal.png")
            self.en_boton.source = self.app.get_path_resources(
                "ingles", "boton_ingles_down.png")

        self.esp_boton.reload()
        self.en_boton.reload()


    def on_enter(self, *args):
        try:
            self.app.load_audio("2.wav")
            self.app.play_audio()
        except AttributeError:
            self.on_enter()
        # @TODO Implementar el salvapantallas con el Clock
        return super().on_enter(*args)
    
    def on_pre_leave(self, *args):
        if self.app.audio_file:
            self.app.stop_audio()
        return super().on_pre_leave(*args)