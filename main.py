from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

# from kivy.core.window import Window
# Window.maximize()
from src.screens.mainScreen import MainScreen
from src.screens.menu_esp import MenuEsp
from src.screens.salvaPantallas import SalvaPantalla
from src.settings.local import langs

Window.size = (640, 360)


class MainApp(MDApp):
    data_page = {}
    screen_manager = ScreenManager()

    def __init__(self, **kwargs):
        self.set_language()
        super().__init__(**kwargs)

    def build(self):
        """
           docstring
        """

        self.theme_cls.primary_palette = 'BlueGray'

        self.screen_manager.add_widget(SalvaPantalla(name='salvaPantallas'))  # Pantalla 1
        self.screen_manager.add_widget(MainScreen(name='mainScreen'))  # Pantalla 2
        self.screen_manager.add_widget(MenuEsp(name='menu_esp'))  # Pantalla 3

        self.screen_manager.current = 'mainScreen'
        return self.screen_manager

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
        self.screen_manager.clear_widgets(screens=[self.screen_manager.get_screen(screen)])
        if screen == 'menu_esp':
            page = MenuEsp(name='menu_esp')
        elif screen == 'menu_abc':
            page = MenuABC(name='menu_esp')

        self.screen_manager.add_widget(page)

    def change_screen(self, dt: str = 'mainScreen'):
        self.screen_manager.current = dt
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
    MainApp().run()
