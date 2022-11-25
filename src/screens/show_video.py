from random import randint
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.video import Video

Builder.load_file('src/screens/show_video.kv')


class ShowVideoScreen(Screen):
    """
    Video player
    """
    random_video_number = 1

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
        self.video.source =self.app.get_path_resources(res_type='video', file=f'{randint(1,4)}.mp4')

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
            self.app.sm.current = "game_mode"


    
