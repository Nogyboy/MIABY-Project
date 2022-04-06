from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.app import App

# from kivy.core.window import Window
# Window.maximize()
from src.screens.mainScreen import MainScreen
from src.screens.menu_esp import MenuEsp
from src.screens.salvaPantallas import SalvaPantalla
from src.settings.local import langs

Window.size = (640, 360)


class MainApp(App):
    data_page = {}
    sm = ScreenManager()

    def __init__(self, **kwargs):
        self.set_language()
        super().__init__(**kwargs)

    def build(self):
        """
           docstring
        """

        self.sm.add_widget(SalvaPantalla(name='salvaPantallas'))  # Pantalla 1
        self.sm.add_widget(MainScreen(name='mainScreen'))  # Pantalla 2
        self.sm.add_widget(MenuEsp(name='menu_esp'))  # Pantalla 3

        self.sm.current = 'mainScreen' # Pantalla inicial
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
    MainApp().run()
