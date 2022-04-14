# App
from src.settings.local import langs
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivy.app import App

# Screens
from src.screens.inicio import InicioScreen
from src.screens.modo_juego import ModoJuegoScreen
from src.screens.salvaPantallas import SalvaPantalla


# Configuración Local de la Aplicación
from kivy.config import Config

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

KIVY_CONFIG = str(BASE_DIR.joinpath('miaby.ini'))

IMG_PATH = BASE_DIR.joinpath('resources','img')

Config.read(KIVY_CONFIG)


class MIABYApp(App):
    info_screen = {}
    sm = ScreenManager()  # Manejador de Pantallas
    idioma = "Nulo"

    def build_config(self, config):
        """
        Construir un archivo de configuraciones local .ini de la aplicación.
        
        """
        config.setdefaults('kivy', {
            'default_font': "['Roboto', 'data/fonts/Roboto-Regular.ttf', 'data/fonts/Roboto-Italic.ttf', 'data/fonts/Roboto-Bold.ttf', 'data/fonts/Roboto-BoldItalic.ttf']",
            'log_dir': 'logs',
            'log_enable': 1,
            'log_level': 'info',
            'log_name': "kivy_%y-%m-%d_%_.txt"
        })
        config.setdefaults('graphics', {
            'borderless': 1,
            'windows_state': 'visible',
            'fullscreen': 'auto',
            'maxfps': 60,
            'show_cursor': 0,
            'resizable': 1,
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
        self.sm.add_widget(InicioScreen(name='inicio'))
        # self.sm.add_widget(SalvaPantalla(name='salvaPantallas'))
        self.sm.add_widget(ModoJuegoScreen(name='modo_juego'))

        self.sm.current = 'inicio'  # Pantalla inicial
        return self.sm

    def get_path_resources(self, idioma, img):
        """
        Generar el path completo de los recursos para cada S.O.
        """
        return str(IMG_PATH.joinpath(idioma,img))



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

    def change_screen(self, screen: str = 'inicio'):
        self.sm.current = screen
        # if screen_manager.current != 'salvaPantallas':
        #     screen_manager.current = 'salvaPantallas'

    def set_language(self, lang: str = 'es'):
        if not langs.equals(lang):
            langs.set_lang(lang)
            self.change_memomry()

    def change_memomry(self):
        self.info_screen = langs.read_json()
        # for key, value in self.data_page.items():
        #     print(f'{key}: {value}')
        self.refresh('menu_esp')




if __name__ == '__main__':
    MIABYApp().run()
