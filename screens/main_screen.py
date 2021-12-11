from typing import Dict
from typing import List

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.utils import escape_markup

from config.styles import menu_button_style
from config.styles import header_style


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.rounds = 3
        self.teams = set()
        self.rating: Dict[str, Dict[str, int]] = {}
        self.main_screen()

    def main_screen(self):
        layout = GridLayout()
        layout.rows = 2
        label = Label(text='Новогодний музыкальный конкурс', **header_style)

        layout.add_widget(label)
        box_layout = BoxLayout(orientation='vertical')
        box_layout.spacing = 5
        box_layout.padding = 10
        users = Button(text='Команды', **menu_button_style)
        rules = Button(text='Правила игры', **menu_button_style)
        round1 = Button(text='Раунд I', **menu_button_style)
        round2 = Button(text='Раунд II', **menu_button_style)
        round3 = Button(text='Раунд III', **menu_button_style)
        rating = Button(text='Рейтинг', **menu_button_style)
        users.bind(on_press=self.show_users)
        rules.bind(on_press=self.show_rules)
        round1.bind(on_press=self.play_round)
        round2.bind(on_press=self.play_round)
        round3.bind(on_press=self.play_round)
        rating.bind(on_press=self.show_rating)
        box_layout.add_widget(users)
        box_layout.add_widget(rules)
        box_layout.add_widget(round1)
        box_layout.add_widget(round2)
        box_layout.add_widget(round3)
        box_layout.add_widget(rating)
        layout.add_widget(box_layout)
        self.add_widget(layout)

    def show_users(self, instance: Button):
        def save_commands(instance: Button):
            self.teams.clear()
            for text in inputs:
                text.disabled = True
                if text.text is not None and text.text != '':
                    self.teams.add(text.text)
            self._init_rating()

        main_layout = BoxLayout(orientation='vertical')
        main_layout.spacing = 10
        main_layout.padding = 10
        label = Label(text='Задайте названия команд: \n'
                           '    -максимальное количество команд = 4; \n'
                           '    -для сохранения названия нажмите "Сохранить"; \n'
                           '    -если у Вас число команд меньше 4, то оставьте остальные поля пустыми.',
                      size_hint=(1, 0.2),
                      font_size='20sp',
                      size=(100, 30), )

        teams_layout = GridLayout()
        teams_layout.cols = 1
        teams_layout.rows = 5
        teams_layout.spacing = 10
        teams_layout.padding = 20
        inputs: List[TextInput] = []
        teams = list(self.teams)
        disabled = len(teams) > 0
        for i in range(teams_layout.rows - 1):
            try:
                text = teams[i]
            except IndexError:
                text = ''
            text_input = TextInput(
                text=text,
                multiline=False,
                size_hint=(0.8, 0.2),
                size=(100, 20),
                font_size='25sp',
                halign='center',
                disabled=disabled
            )
            inputs.append(text_input)
            teams_layout.add_widget(text_input)
        save_button = Button(text='Сохранить', **menu_button_style, size_hint=(1, 0.3), size=(100, 30), disabled=disabled)
        save_button.bind(on_press=save_commands)
        teams_layout.add_widget(save_button)

        close_button = Button(text='Закрыть', **menu_button_style, size_hint=(1, 0.2), size=(100, 30), )
        main_layout.add_widget(label)
        main_layout.add_widget(teams_layout)
        popup = Popup(title='Команды', content=main_layout, auto_dismiss=False)
        close_button.bind(on_press=popup.dismiss)
        main_layout.add_widget(close_button)
        popup.open()

    def show_rules(self, btn: Button):
        layout = BoxLayout(orientation='vertical')
        rules = Label(text='Правила игры\nЗдесь надо написать \nправила\nигры')
        close_button = Button(text='Закрыть', **menu_button_style, size_hint=(0.3, 0.1), size=(100, 30), )
        layout.add_widget(rules)
        layout.add_widget(close_button)
        popup = Popup(title='Правила игры', content=layout, auto_dismiss=False)
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def play_round(self, btn: Button):
        self.manager.transition.direction = 'left'
        self.manager.current = btn.text

    def show_rating(self, btn: Button):
        rating_layout = GridLayout()
        rating_layout.spacing = 10
        rating_layout.padding = 10
        rating_layout.cols = 5
        # fill header
        rating_layout.add_widget(Button(**menu_button_style, disabled=True))
        rating_layout.add_widget(Button(**menu_button_style, disabled=True, text='Раунд I'))
        rating_layout.add_widget(Button(**menu_button_style, disabled=True, text='Раунд II'))
        rating_layout.add_widget(Button(**menu_button_style, disabled=True, text='Раунд III'))
        rating_layout.add_widget(Button(**menu_button_style, disabled=True, text='Итого'))
        commands = sorted(list(self.teams))
        winner_command, max_sum = None, 0
        for c in commands:
            c_total_rating = self._count_total_rating(c)
            if c_total_rating > max_sum:
                winner_command = c
                max_sum = c_total_rating
        winner_color = (1, 1, 0, 1)
        for command in commands:
            rating_layout.add_widget(Button(**menu_button_style, disabled=True, text=command))
            rating_layout.add_widget(Button(**menu_button_style, disabled=True, text=str(self.rating[command]['Раунд I'])))
            rating_layout.add_widget(Button(**menu_button_style, disabled=True, text=str(self.rating[command]['Раунд II'])))
            rating_layout.add_widget(Button(**menu_button_style, disabled=True, text=str(self.rating[command]['Раунд III'])))
            if command == winner_command:
                rating_layout.add_widget(Button(**{
                    'font_size': '28sp',
                    'background_color': winner_color
                }, disabled=True, text=str(max_sum)))
            else:
                rating_layout.add_widget(
                    Button(**menu_button_style, disabled=True, text=str(self._count_total_rating(command))))
        close_button = Button(text='Закрыть', **menu_button_style, size_hint=(1, 0.2), size=(100, 30), )
        popup = Popup(title='Команды', content=rating_layout, auto_dismiss=False)
        close_button.bind(on_press=popup.dismiss)
        rating_layout.add_widget(close_button)
        popup.open()

    def _count_total_rating(self, command: str) -> int:
        rounds = self.rating[command]
        return sum([rounds[value] for value in rounds])

    def _init_rating(self):
        self.rating = {team: {
            'Раунд I': 0,
            'Раунд II': 0,
            'Раунд III': 0,
        } for team in self.teams}
