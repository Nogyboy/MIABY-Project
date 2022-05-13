from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import (ObjectProperty)
from kivy.app import App


Builder.load_file('src/screens/modo_juego.kv')


class ModoJuegoScreen(Screen):
    observar_boton = ObjectProperty(None)
    aprender_boton = ObjectProperty(None)
    interactuar_boton = ObjectProperty(None)
    background = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()

    def update_image_buttons_mode(self, option, lang):
        """
        Actualiza la imagen del botón en función de la
        opción que se encuentre actualmente seleccionada.
        """
        if option == "observar":
            self.observar_boton.source = self.app.get_path_resources(
                lang, "boton_observar_down.png")
            self.aprender_boton.source = self.app.get_path_resources(
                lang, "boton_aprender_normal.png")
            self.interactuar_boton.source = self.app.get_path_resources(
                lang, "boton_interactuar_normal.png")
        elif option == "aprender":
            self.observar_boton.source = self.app.get_path_resources(
                lang, "boton_observar_normal.png")
            self.aprender_boton.source = self.app.get_path_resources(
                lang, "boton_aprender_down.png")
            self.interactuar_boton.source = self.app.get_path_resources(
                lang, "boton_interactuar_normal.png")
        elif option == "interactuar":
            self.observar_boton.source = self.app.get_path_resources(
                lang, "boton_observar_normal.png")
            self.aprender_boton.source = self.app.get_path_resources(
                lang, "boton_aprender_normal.png")
            self.interactuar_boton.source = self.app.get_path_resources(
                lang, "boton_interactuar_down.png")

        self.background.source = self.app.get_path_resources(
                lang, "modo_juego.png")

        self.background.reload()
        self.observar_boton.reload()
        self.aprender_boton.reload()
        self.interactuar_boton.reload()

    def on_enter(self, *args):
        self.app.load_audio("3.wav")
        self.app.play_audio()
        return super().on_enter(*args)
    
    def on_pre_leave(self, *args):
        if self.app.audio_file:
            self.app.stop_audio()
        return super().on_pre_leave(*args)