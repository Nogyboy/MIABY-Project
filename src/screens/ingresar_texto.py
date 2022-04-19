from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import (ObjectProperty)

Builder.load_file('src/screens/ingresar_texto.kv')


class IngresarTextoScreen(Screen):

    background = ObjectProperty(None)
    input_text = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()

    def update_background_image(self, lang):
        """
        Actualiza la imagen de fondo en función del idioma.
        """
        self.background.source = self.app.get_path_resources(lang, "introducir_palabra.png")

        self.background.reload()

    
    def validate_word_entry(self, letter):
        """
        Ingresa y valida la letra de la palabra elegida.
        """
        
        actual_words = len(self.input_text.text)
        try:
            if letter == self.app.word_selected[actual_words]:
                self.input_text.text = self.input_text.text + letter
                if self.input_text.text == self.app.word_selected:
                    self.app.sm.current = "mensaje"
                    self.input_text.text = ""
            else:
                pass
        except IndexError:
            print("Palabra terminada.")

    
    def on_enter(self, *args):
        try:
            self.app.load_audio("10.wav")
            self.app.play_audio()
        except AttributeError:
            self.on_enter()
        return super().on_enter(*args)
    
    def on_pre_leave(self, *args):
        if self.app.audio_file:
            self.app.stop_audio()
        return super().on_pre_leave(*args)
