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

    def select_word(self, code):
        """
        Asigna la palabra según el idioma para luego
        ser deletreada.
        """
        app = App.get_running_app()
        app.word_selected = app.words[code]
        del app
        
    def on_enter(self, *args):
        # @TODO Implementar la lectura de las tarjetas cuando entra a esta pantalla, se podría cancelar
        # con la tecla de regreso.
        self.select_word("7")
        
        return super().on_enter(*args)