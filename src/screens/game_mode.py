from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import (ObjectProperty)
from kivy.app import App


Builder.load_file('src/screens/game_mode.kv')


class GameModeScreen(Screen):
    observe_button = ObjectProperty(None)
    learning_button = ObjectProperty(None)
    interact_button = ObjectProperty(None)
    background = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()

    def update_image_buttons_mode(self, option):
        """
        Update selected button.
        """

        def get_image_path(button):
            if option == button:
                return(f"button_{option}_down.png")
            else:
                return(f"button_{button}_normal.png")

        self.observe_button.source = self.app.get_path_resources(
            "images", get_image_path("observe"))
        self.learning_button.source = self.app.get_path_resources(
            "images", get_image_path("learning"))
        self.interact_button.source = self.app.get_path_resources(
            "images", get_image_path("interact"))


        self.background.source = self.app.get_path_resources("images","game_mode.png")

        self.background.reload()
        self.observe_button.reload()
        self.learning_button.reload()
        self.interact_button.reload()

    def on_enter(self, *args):
        self.app.load_audio("3.wav")
        self.app.play_audio()
        return super().on_enter(*args)
    
    def on_pre_leave(self, *args):
        if self.app.audio_file:
            self.app.stop_audio()
        return super().on_pre_leave(*args)