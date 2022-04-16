from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import (ObjectProperty)

import json
from icecream import ic


Builder.load_file('src/screens/inicio.kv')


class InicioScreen(Screen):

    esp_boton = ObjectProperty(None)
    en_boton = ObjectProperty(None)

    def choose_language(self, lang):
        """
        Selección de idioma, se almacena en la variable idioma de la clase
        MIABYApp.
        """
        app = App.get_running_app()
        path_json_words = app.get_path_resources("words","data.json")

        with open(path_json_words, encoding="utf-8") as file:
            app.words = json.load(file)[lang]

        del app

    def update_image_buttons_language(self, option):
        """
        Actualiza la imagen del botón en función de la
        opción que se encuentre actualmente seleccionada.
        """
        app = App.get_running_app()
        if option == "español":
            self.esp_boton.source = app.get_path_resources(
                "español", "boton_esp_down.png")
            self.en_boton.source = app.get_path_resources(
                "ingles", "boton_ingles_normal.png")
        elif option == "ingles":
            self.esp_boton.source = app.get_path_resources(
                "español", "boton_esp_normal.png")
            self.en_boton.source = app.get_path_resources(
                "ingles", "boton_ingles_down.png")

        self.esp_boton.reload()
        self.en_boton.reload()

        del app
