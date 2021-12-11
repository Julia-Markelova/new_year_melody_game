from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from config import colors
from screens.main_screen import MainScreen
from screens.round_screen import RoundScreen
from tasks.categories import configure_categories


# class MainScreen(Screen):
#     def __init__(self, **kwargs):
#         super(MainScreen, self).__init__(**kwargs)
#         self.rounds = 3
#         self.teams = 0
#         self.results = {}
#         self.categories: List[Category] = configure_categories()
#         self.main_screen()
#
#     def main_screen(self):
#         self.rows = 6
#         label = Label(text='[b][color=black]' + escape_markup('Новогодний музыкальный конкурс') + '[/color][/b]',
#                       markup=True,
#                       font_size='20sp',
#                       )
#
#         self.add_widget(label)
#         box_layout = BoxLayout(orientation='vertical')
#         box_layout.spacing = 5
#         box_layout.padding = 10
#         users = Button(text='Команды', **button_style)
#         rules = Button(text='Правила игры', **button_style)
#         round1 = Button(text='Раунд I', **button_style)
#         round2 = Button(text='Раунд II', **button_style)
#         round3 = Button(text='Раунд III', **button_style)
#         rating = Button(text='Рейтинг', **button_style)
#         rules.bind(on_press=self.show_rules)
#         round1.bind(on_press=self.play_round)
#         rating.bind(on_press=self.show_rating)
#         box_layout.add_widget(users)
#         box_layout.add_widget(rules)
#         box_layout.add_widget(round1)
#         box_layout.add_widget(round2)
#         box_layout.add_widget(round3)
#         box_layout.add_widget(rating)
#         self.add_widget(box_layout)
#
#     def set_users(self):
#         def on_enter(instance, value):
#             print('User pressed enter in', instance, 'value ', value)
#         layout = BoxLayout(orientation='vertical')
#         label = Label(text='Команды')
#         text_input = TextInput(text='Hello world')
#         text_input.bind(on_enter=on_enter)
#
#
#     def show_rules(self, btn: Button):
#         popup = Popup(content=Label(text='Правила игры'))
#         popup.open()
#
#     def play_round(self, btn: Button):
#         layout = GridLayout()
#         self._configure_round_layout(layout)
#         main_menu_button = Button(text='Завершить раунд', **button_style)
#         box_layout = BoxLayout(orientation='vertical')
#         box_layout.spacing = 5
#         box_layout.padding = 10
#         box_layout.add_widget(layout)
#         box_layout.add_widget(main_menu_button)
#         popup = Popup(content=box_layout, auto_dismiss=False)
#         main_menu_button.bind(on_press=popup.dismiss)
#         popup.open()
#
#     def show_rating(self, btn: Button):
#         pass
#
#     def on_btn_pressed(self, instance: Button):
#         instance.disabled = True
#         content = Button(text='Close me!', size=(300, 80),
#                          size_hint=(None, None))
#         popup = Popup(content=content, auto_dismiss=False)
#         content.bind(on_press=popup.dismiss)
#         popup.open()
#
#     def _configure_round_layout(self, layout: GridLayout):
#         layout.padding = 10
#         layout.spacing = 3
#         layout.cols = len(self.categories[0].tasks) + 1
#         layout.rows = len(self.categories)
#
#         for category in self.categories:
#             layout.add_widget(Label(text='[b][color=black]' + escape_markup(category.name) + '[/color][/b]',
#                                     markup=True,
#                                     font_size='20sp',
#                                     )
#                               )
#
#             for task in category.tasks:
#                 button = Button(text=str(task.point_count),
#                                 font_size='28sp',
#                                 background_color=(0.02, 0.02, 1, 1),
#                                 )
#                 button.bind(on_press=self.on_btn_pressed if task.handler is None else task.handler)
#                 layout.add_widget(button)


class MyApp(App):
    def build(self):
        screen_manager = ScreenManager()
        main_screen = MainScreen(name='Main Screen')

        first_round_screen = RoundScreen(name='Раунд I', categories=configure_categories(1))
        second_round_screen = RoundScreen(name='Раунд II', categories=configure_categories(2))
        third_round_screen = RoundScreen(name='Раунд III', categories=configure_categories(3))

        screen_manager.add_widget(main_screen)
        screen_manager.add_widget(first_round_screen)
        screen_manager.add_widget(second_round_screen)
        screen_manager.add_widget(third_round_screen)
        return screen_manager


if __name__ == '__main__':
    Window.clearcolor = colors.theme_1_white
    MyApp().run()
