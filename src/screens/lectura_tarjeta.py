from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.video import Video
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from kivy.clock import Clock

Builder.load_file('src/screens/lectura_tarjeta.kv')


class LecturaTarjetaScreen(Screen):
    
    before_lang = ""
    reader = SimpleMFRC522()
    secs = 0
    event = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        self.image_vid_esp = Video(source=self.app.get_path_resources('español','leer_tarjeta.mp4'), pos=self.pos, size=self.size, nocache=True, state="stop", options = {'eos': 'loop'}, allow_stretch=True)
        self.image_vid_en = Video(source=self.app.get_path_resources('ingles','leer_tarjeta.mp4'),pos=self.pos, size=self.size, nocache=True, state="stop", options = {'eos': 'loop'}, allow_stretch=True)
        

    def update_background_image(self, lang):
        """
        Actualiza la imagen de fondo en función del idioma.
        """
        if lang =="español":
            if not(self.before_lang == lang):
                self.remove_widget(self.image_vid_en)
                self.add_widget(self.image_vid_esp)
            self.before_lang = lang
        elif lang == "ingles":
            if not(self.before_lang == lang):
                self.add_widget(self.image_vid_en)
                self.remove_widget(self.image_vid_esp)
            self.before_lang = lang

    def select_word(self, code):
        """
        Asigna la palabra según el idioma para luego
        ser deletreada.
        """
        self.app.word_selected = self.app.words[code]
        
    def update_time_read_card(self, sec):
        """
        Contador de tiempo de lectura de tarjeta.
        """
        self.secs = self.secs+1
        id, text = self.reader.read_no_block()
        if self.secs == 40:
            self.event.cancel()
            self.secs = 0
            self.app.sm.current = "modo_juego"
        elif id != None:
            self.event.cancel()
            self.secs = 0
            self.select_word(text)
            self.app.sm.current = "ingresar_texto"


    def on_enter(self, *args):
        """
        Al entrar en la pantalla iniciar la animacion
        """
        if self.app.inicio_option == "español":
            self.image_vid_esp.state = "play"
        elif self.app.inicio_option == "ingles":
            self.image_vid_en.state = "play"

        self.app.load_audio("9.wav")
        self.app.play_audio()

        self.event = Clock.schedule_interval(self.update_time_read_card, 0.5)
        # @TODO Implementar la lectura de las tarjetas cuando entra a esta pantalla, se podría cancelar
        # con la tecla de regreso.
        
        return super().on_enter(*args)

    def on_pre_leave(self, *args):
        if self.app.audio_file:
            self.app.stop_audio()
        return super().on_pre_leave(*args)

    def on_leave(self, *args):
        """
        Al salir de la pantalla detener la animacion
        """
        self.image_vid_esp.state = "stop"
        self.image_vid_en.state = "stop"
        return super().on_leave(*args)