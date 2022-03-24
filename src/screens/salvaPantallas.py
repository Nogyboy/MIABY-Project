from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton

from src.settings import PATH_VIDEOS

Builder.load_string("""
<SalvaPantalla>:
    Video:
        source: root.video_path
        state: root.state
        options: root.options
        allow_stretch: root.allow_stretch
        volume: root.volume
        fullscreen: root.fullscreen
""")


class SalvaPantalla(Screen):
    video_path = str(PATH_VIDEOS / 'caritafeli.mp4')
    state = 'play'
    options = {'eos': 'loop'}
    allow_stretch = True
    fullscreen = True
    volume = 0
