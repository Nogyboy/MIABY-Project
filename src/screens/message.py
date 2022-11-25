from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

Builder.load_file('src/screens/message.kv')


class MessageScreen(Screen, FloatLayout):
    secs = 0
    event = None
    before_lang = ""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        self.image_message = Image(source=self.app.get_path_resources(
            "images", "message.png"), pos=self.pos, size=self.size)
        self.add_widget(self.image_message)

    def update_time(self, sec):
        """
        Timer to see the message.
        """
        self.secs = self.secs+1
        if self.secs == 5:
            self.event.cancel()
            self.secs = 0
            self.app.sm.current = "read_card"

    def on_enter(self):
        """
        Start timer.
        """
        self.event = Clock.schedule_interval(self.update_time, 1)

    def update_image(self):
        """
        Update background image.
        """
        self.image_message.source = self.app.get_path_resources(
            "images", "message.png")
        self.image_message.reload()
