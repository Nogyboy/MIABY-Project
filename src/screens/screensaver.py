from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.image import Image

class ScreenSaverScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        self.video_screensaver = Image(source=self.app.get_path_resources('common','inactivity_animation.png'), pos=self.pos, size=self.size)
        self.add_widget(self.video_screensaver)
