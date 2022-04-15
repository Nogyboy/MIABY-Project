from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import (ObjectProperty)
from kivy.app import App


Builder.load_file('src/screens/lectura_tarjeta.kv')


class LecturaTarjetaScreen(Screen):
    background = ObjectProperty(None)

    def update_background_image(self, lang):
        """
        Actualiza la imagen de fondo en función del idioma.
        """
        app = App.get_running_app()
        self.background.source = app.get_path_resources(lang, "leer_tarjeta.png")

        self.background.reload()

        del app