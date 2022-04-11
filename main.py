from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivy.app import App

from src.screens.mainScreen import MainScreen
from src.screens.menu_esp import MenuEsp
from src.screens.salvaPantallas import SalvaPantalla
from src.settings.local import langs


# Configuración Local de la Aplicación
from kivy.config import Config

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KIVY_CONFIG = os.path.join(BASE_DIR, 'miaby.ini')

Config.read(KIVY_CONFIG)

class MIABYApp(App):
    data_page = {}
    sm = ScreenManager()  # Manejador de Pantallas

    def __init__(self, **kwargs):
        self.set_language()
        super().__init__(**kwargs)

    def build_config(self, config):
        config.setdefaults('kivy', {
            'default_font': "['Roboto', 'data/fonts/Roboto-Regular.ttf', 'data/fonts/Roboto-Italic.ttf', 'data/fonts/Roboto-Bold.ttf', 'data/fonts/Roboto-BoldItalic.ttf']",
            'log_dir': 'logs',
            'log_enable': 1,
            'log_level': 'info',
            'log_name': "kivy_%y-%m-%d_%_.txt"
        })
        config.setdefaults('graphics', {
            'borderless':1,
            'windows_state':'visible',
            'fullscreen':'auto',
            'maxfps':60,
            'show_cursor':0,
            'resizable':1,
        })

    def build(self):
        """
           Construcción de intefaces
            - Inicio
            - Modo de Juego
            - Modo - Observar
            - Modo - Aprender
            - Modo - Practicar
        """

        # self.sm.add_widget(SalvaPantalla(name='salvaPantallas'))
        self.sm.add_widget(MainScreen(name='mainScreen'))
        self.sm.add_widget(MenuEsp(name='menu_esp'))

        self.sm.current = 'mainScreen'  # Pantalla inicial
        return self.sm

    def on_start(self):
        """
           docstrin
        """
        # self.event = Clock.schedule_once(self.change_screen, 5)

    def reset_clock(self):
        """
            docstrin
        """
        Clock.unschedule(self.event)
        self.on_start()

    def refresh(self, screen):
        global page
        self.sm.clear_widgets(screens=[self.sm.get_screen(screen)])
        if screen == 'menu_esp':
            page = MenuEsp(name='menu_esp')
        elif screen == 'menu_abc':
            page = MenuABC(name='menu_esp')

        self.sm.add_widget(page)

    def change_screen(self, dt: str = 'mainScreen'):
        self.sm.current = dt
        # if screen_manager.current != 'salvaPantallas':
        #     screen_manager.current = 'salvaPantallas'

    def set_language(self, lang: str = 'es'):
        if not langs.equals(lang):
            langs.set_lang(lang)
            self.change_memomry()

    def change_memomry(self):
        self.data_page = langs.read_json()
        for key, value in self.data_page.items():
            print(f'{key}: {value}')
        self.refresh('menu_esp')


if __name__ == '__main__':
    MIABYApp().run()
