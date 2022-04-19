from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.video import Video

class BienvenidaScreen(Screen):

    image_bienvenida = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        self.image_bienvenida = Video(source=self.app.get_path_resources('common','animacion_inicio.mp4'), pos=self.pos, size=self.size,nocache=True, state="play", options = {'eos': 'loop'}, allow_stretch=True)
        self.add_widget(self.image_bienvenida)

    def on_leave(self, *args):
        self.image_bienvenida.anim_delay = -1
        return super().on_leave(*args)

