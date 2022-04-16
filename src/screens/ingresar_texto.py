from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import (ObjectProperty)

Builder.load_file('src/screens/ingresar_texto.kv')


class IngresarTextoScreen(Screen):

    background = ObjectProperty(None)
    input_text = ObjectProperty(None)

    def update_background_image(self, lang):
        """
        Actualiza la imagen de fondo en función del idioma.
        """
        app = App.get_running_app()
        self.background.source = app.get_path_resources(lang, "introducir_palabra.png")

        self.background.reload()

        del app
    
    def validate_word_entry(self, letter):
        """
        Ingresa y valida la letra de la palabra elegida.
        """
        app = App.get_running_app()
        actual_words = len(self.input_text.text)
        try:
            if letter == app.word_selected[actual_words]:
                self.input_text.text = self.input_text.text + letter
                if self.input_text.text == app.word_selected:
                    app.sm.current = "mensaje"
                    self.input_text.text = ""
            else:
                pass
        except IndexError:
            print("Palabra terminada.")
        finally:
            del app
