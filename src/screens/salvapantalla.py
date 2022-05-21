from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.video import Video

class SalvaPantallaScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        self.video_salvapantallas = Video(source=self.app.get_path_resources('common','animacion_inicio.mp4'), pos=self.pos, size=self.size,nocache=True, state="stop", options = {'eos': 'loop'}, allow_stretch=True)
        self.add_widget(self.video_salvapantallas)

    def on_enter(self, *args):
        self.video_salvapantallas.state = "play"
        return super().on_enter(*args)

    def on_leave(self, *args):
        self.video_salvapantallas.state = "stop"
        return super().on_leave(*args)

