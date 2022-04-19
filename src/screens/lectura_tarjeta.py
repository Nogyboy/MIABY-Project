from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import (ObjectProperty)
from kivy.app import App
from kivy.uix.image import AsyncImage

Builder.load_file('src/screens/lectura_tarjeta.kv')


class LecturaTarjetaScreen(Screen):
    
    before_lang = ""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        self.image_gif_esp = AsyncImage(source=self.app.get_path_resources('español','leer_tarjeta.gif'), pos=self.pos, size=self.size, keep_ratio=False, keep_data=True, anim_delay=-1, anim_loop=1)
        self.image_gif_en = AsyncImage(source=self.app.get_path_resources('ingles','leer_tarjeta.gif'),pos=self.pos, size=self.size, keep_ratio=False, keep_data=True, anim_delay=-1, anim_loop=1)
        

    def update_background_image(self, lang):
        """
        Actualiza la imagen de fondo en función del idioma.
        """
        if lang =="español":
            if not(self.before_lang == lang):
                self.remove_widget(self.image_gif_en)
                self.add_widget(self.image_gif_esp)
            self.before_lang = lang
        elif lang == "ingles":
            if not(self.before_lang == lang):
                self.add_widget(self.image_gif_en)
                self.remove_widget(self.image_gif_esp)
            self.before_lang = lang

    def select_word(self, code):
        """
        Asigna la palabra según el idioma para luego
        ser deletreada.
        """
        self.app.word_selected = self.app.words[code]
        
    def on_enter(self, *args):
        """
        Al entrar en la pantalla iniciar la animacion
        """
        if self.app.inicio_option == "español":
            self.image_gif_esp.anim_delay = 0.10
        elif self.app.inicio_option == "ingles":
            self.image_gif_en.anim_delay = 0.10

        self.app.load_audio("9.wav")
        self.app.play_audio()
        # @TODO Implementar la lectura de las tarjetas cuando entra a esta pantalla, se podría cancelar
        # con la tecla de regreso.
        self.select_word("7")
        
        return super().on_enter(*args)

    def on_pre_leave(self, *args):
        if self.app.audio_file:
            self.app.stop_audio()
        return super().on_pre_leave(*args)

    def on_leave(self, *args):
        """
        Al salir de la pantalla detener la animacion
        """
        self.image_gif_esp.anim_delay =  -1
        return super().on_leave(*args)