from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.video import Video

Builder.load_file('src/screens/mostrar_video.kv')


class MostrarVideoScreen(Screen):
    """
    Reproductor de video
    """

    def __init__(self, **kw):
        self.app = App.get_running_app()
        self.video = Video(source=self.app.get_path_resources(tipo='video', file='2.mp4'),pos=self.pos, size=self.size)
        self.add_widget(self.video)
        super().__init__(**kw)
    
    def on_enter(self, *args):
        self.video.state = "play"
        return super().on_enter(*args)

    