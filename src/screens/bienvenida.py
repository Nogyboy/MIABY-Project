from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.video import Video

class BienvenidaScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        self.video_bienvenida = Video(source=self.app.get_path_resources('common','animacion_inicio.mp4'), pos=self.pos, size=self.size,nocache=True, state="play", options = {'eos': 'loop'}, allow_stretch=True)
        self.add_widget(self.video_bienvenida)

    def on_leave(self, *args):
        self.video_bienvenida.state = "stop"
        return super().on_leave(*args)

