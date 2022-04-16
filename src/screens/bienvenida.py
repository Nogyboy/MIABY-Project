from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage


class BienvenidaScreen(Screen, FloatLayout):

    image_bienvenida = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        self.image_bienvenida = AsyncImage(source=self.app.get_path_resources('common','animacion_inicio.gif'), pos=self.pos, size=self.size, keep_ratio=False, keep_data=True, anim_delay=0.10, anim_loop=1)
        self.add_widget(self.image_bienvenida)

    def on_leave(self, *args):
        self.image_bienvenida.anim_delay = -1
        return super().on_leave(*args)

