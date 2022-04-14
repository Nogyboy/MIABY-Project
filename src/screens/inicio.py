from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import (ObjectProperty)

# from playsound import playsound

from kivy.uix.behaviors import FocusBehavior

Builder.load_file('src/screens/inicio.kv')

# class FocusButton(FocusBehavior, Button):
#    pass


class InicioScreen(Screen):

    esp_boton = ObjectProperty(None)
    en_boton = ObjectProperty(None)

    def choose_language(self, lang: str = 'es'):
        """
        Selección de idioma, se almacena en la variable idioma de la clase
        MIABYApp.
        """
        app = App.get_running_app()
        app.language = lang

        del app

    def update_image_buttons_languaje(self, option):
        """
        Actualiza la imagen del botón en función de la
        opción que se encuentre actualmente seleccionada.
        """
        app = App.get_running_app()
        if option == "español":
            self.esp_boton.source = app.get_path_resources(
                "esp", "boton_esp_down.png")
            self.en_boton.source = app.get_path_resources(
                "en", "boton_ingles_normal.png")
        elif option == "ingles":
            self.esp_boton.source = app.get_path_resources(
                "esp", "boton_esp_normal.png")
            self.en_boton.source = app.get_path_resources(
                "en", "boton_ingles_down.png")

        self.esp_boton.reload()
        self.en_boton.reload()

        del app


# @TODO Contrustruir el método para cargar la información de las palabra en función del idioma desde aquí
