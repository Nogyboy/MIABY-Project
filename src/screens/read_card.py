from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.image import Image

from src.screens import READ_CAR_MODE

if READ_CAR_MODE:
    from mfrc522 import SimpleMFRC522
from kivy.clock import Clock

Builder.load_file('src/screens/lectura_tarjeta.kv')


class LecturaTarjetaScreen(Screen):
    
    if READ_CAR_MODE:
        reader = SimpleMFRC522()
    secs = 0
    event = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        self.img_lectura = Image(source=self.app.get_path_resources("español","leer_tarjeta.png"), pos=self.pos, size=self.size)
        self.add_widget(self.img_lectura)   

    def update_background_image(self, lang):
        """
        Actualiza la imagen de fondo en función del idioma.
        """
        self.img_lectura.source = self.app.get_path_resources(lang,"leer_tarjeta.png")
        self.img_lectura.reload()

    def select_word(self, code):
        """
        Asigna la palabra según el idioma para luego
        ser deletreada.
        """
        self.app.word_selected = self.app.words[str(code)]
        
    def update_time_read_card(self, sec):
        """
        Contador de tiempo de lectura de tarjeta.
        """
        self.secs = self.secs+1
        id, text = self.reader.read_no_block()
        if self.secs == 40:
            try:
                self.event.cancel()
            except AttributeError:
                print("No existe la instancia...")
            self.secs = 0
            self.app.sm.current = "modo_juego"

        elif id != None:
            self.event.cancel()
            self.secs = 0
            self.select_word(int(text))
            self.app.sm.current = "ingresar_texto"


    def on_enter(self, *args):
        """
        Al entrar reproducir el audio e iniciar la lectura de la tarjeta
        """

        self.app.load_audio("7.wav")
        self.app.play_audio()
        if READ_CAR_MODE:
            self.event = Clock.schedule_interval(self.update_time_read_card, 0.5)
        else:
            self.select_word(1)
            self.app.sm.current = "ingresar_texto"

        
        return super().on_enter(*args)

    def on_pre_leave(self, *args):
        if self.app.audio_file:
            self.app.stop_audio()
        return super().on_pre_leave(*args)
