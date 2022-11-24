from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

Builder.load_file('src/screens/mensaje.kv')


class MensajeScreen(Screen, FloatLayout):
    secs = 0
    event = None
    before_lang = ""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        self.img_mensaje = Image(source=self.app.get_path_resources("español", "mensaje.png"), pos=self.pos, size=self.size)
        self.add_widget(self.img_mensaje)
    def update_time(self, sec):
        """
        Contador de tiempo de visualización del mensaje.
        """
        self.secs = self.secs+1
        if self.secs == 5:
            self.event.cancel()
            self.secs = 0
            self.app.sm.current = "lectura_tarjeta"
 
    def on_enter(self):
        """
        Inicio del contador y la animación.
        """
        self.event = Clock.schedule_interval(self.update_time, 1)


    def update_gif(self, lang):
        """
        Actualizar archivo gif del mensaje.
        """
        self.img_mensaje.source = self.app.get_path_resources(lang,"mensaje.png")
        self.img_mensaje.reload()

        