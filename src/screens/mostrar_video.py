from random import randint
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.video import Video

Builder.load_file('src/screens/mostrar_video.kv')


class MostrarVideoScreen(Screen):
    """
    Reproductor de video
    """
    random_video_number = 1 # Número de video seleccionado

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        self.video = Video(pos=self.pos, size=self.size)
        self.video.bind(
               position=self.on_position_change
                )        
        self.select_random_video()
        self.add_widget(self.video)
    
    def select_random_video(self):
        if self.app.current_option_mode == "aprender":
            self.random_video_number = randint(1,3)
        elif self.app.current_option_mode == "observar":
            self.random_video_number = randint(1,5)
        self.video.source =self.app.get_path_resources(tipo='video', file=f'{self.random_video_number}.mp4')

    def on_enter(self, *args):
        self.video.state = "play"
        return super().on_enter(*args)

    def on_leave(self, *args):
        self.video.state = "stop"
        self.video.unload()
        return super().on_leave(*args)

    def on_position_change(self, instance, value):
        goal = self.video.duration-1
        if value>goal:
            self.app.sm.current = "modo_juego"


    
