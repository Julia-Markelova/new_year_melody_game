from typing import List

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from config import colors
from screens.main_screen import MainScreen
from screens.round_screen import RoundScreen
from tasks.categories import Round
from tasks.categories import configure_rounds

Config.set('kivy', 'exit_on_escape', '0')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class NewYearGameApp(App):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.rating = {}
        main_screen = MainScreen(name='Main Screen')
        screen_manager.add_widget(main_screen)

        rounds: List[Round] = configure_rounds()
        for r in rounds:
            screen = RoundScreen(name=r.get_name(), round_data=r)
            screen_manager.add_widget(screen)

        return screen_manager


if __name__ == '__main__':
    Window.clearcolor = colors.theme_1_white
    NewYearGameApp().run()
