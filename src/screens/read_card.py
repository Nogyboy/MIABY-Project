from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock

Builder.load_file('src/screens/read_card.kv')

DESKTOP_MODE = False

if DESKTOP_MODE:
    from mfrc522 import SimpleMFRC522
    reader = SimpleMFRC522()


class ReadCardScreen(Screen):
    
    secs = 0
    event = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        self.img_read = Image(source=self.app.get_path_resources("images","read_card.png"), pos=self.pos, size=self.size)
        self.add_widget(self.img_read)   

    def update_background_image(self):
        """
        Update background image.
        """
        self.img_read.source = self.app.get_path_resources("images", "read_card.png")
        self.img_read.reload()

    def select_word(self, code):
        """
        Set word to be compared with the input.
        """
        self.app.word_selected = self.app.words[str(code)]
        
    def update_time_read_card(self, sec):
        """
        Time counter for read the card.
        """
        self.secs = self.secs+1
        id, text = self.reader.read_no_block()
        if self.secs == 40:
            try:
                self.event.cancel()
            except AttributeError:
                print("No instance...")
            self.secs = 0
            self.app.sm.current = "game_mode"

        elif id != None:
            self.event.cancel()
            self.secs = 0
            self.select_word(int(text))
            self.app.sm.current = "text_input"


    def on_enter(self, *args):
        """
        Play audio and start reading the card.
        """

        self.app.load_audio("1.wav")
        self.app.play_audio()
        if self.app.config_mode == "board":
            self.event = Clock.schedule_interval(self.update_time_read_card, 0.5)
        else:
            self.select_word(1)
            self.app.sm.current = "text_input"

        
        return super().on_enter(*args)

    def on_pre_leave(self, *args):
        if self.app.audio_file:
            self.app.stop_audio()
        return super().on_pre_leave(*args)
