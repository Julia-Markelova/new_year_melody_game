from kivy.core.audio import Sound
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from config.styles import header_style
from config.styles import melody_button_style
from config.styles import menu_button_style
from config.styles import milk_header_style
from config.styles import round_category_button_style
from config.styles import round_task_button_style
from tasks.categories import Round
from tasks.categories import Task


class RoundScreen(Screen):
    def __init__(self, round_data: Round, **kwargs):
        super().__init__(**kwargs)
        self.round = round_data
        self._configure_round_layout()

    def close_round_screen(self, instance: Button):
        self.manager.transition.direction = 'right'
        self.manager.current = 'Main Screen'

    def _configure_round_layout(self):
        box_layout = BoxLayout(orientation='vertical')
        box_layout.padding = 10
        box_layout.spacing = 10
        title = Label(text=self.name, **header_style, size_hint=(1, 0.1), size=(100, 30), )
        close_btn = Button(text='Завершить раунд', **menu_button_style, size_hint=(1, 0.1), size=(100, 30), )
        close_btn.bind(on_press=self.close_round_screen)

        layout = GridLayout()
        layout.padding = 0
        layout.spacing = 2
        layout.cols = len(self.round.categories[0].tasks) + 1
        layout.rows = len(self.round.categories)

        for category in self.round.categories:
            layout.add_widget(Button(text=category.name, **round_category_button_style))

            for task in category.tasks:
                button = Button(text=str(task.point_count), **round_task_button_style)
                button.bind(on_press=self._default_task_handler(task))
                layout.add_widget(button)

        box_layout.add_widget(title)
        box_layout.add_widget(layout)
        box_layout.add_widget(close_btn)
        self.add_widget(box_layout)

    def _default_task_handler(self, task: Task):
        def handler(instance: Button):
            popup = self._configure_default_popup(task, instance)
            popup.open()

        return handler

    def _configure_default_popup(self, task: Task, instance: Button) -> Popup:
        question_sound: Sound = SoundLoader.load(task.path_to_question)
        answer_sound: Sound = SoundLoader.load(task.path_to_answer)

        def play_sound(sound: Sound, btn: Button):
            if sound:
                answer_player.disabled = True
                question_player.disabled = True
                stopper.disabled = False
                sound.play()

        def stop_sound(btn: Button):
            if question_sound:
                btn.disabled = True
                question_player.disabled = False
                question_sound.stop()
            if answer_sound:
                btn.disabled = True
                answer_player.disabled = False
                answer_sound.stop()

        def reset_melody(btn: Button):
            if question_sound:
                if question_sound.state != 'play':
                    question_player.disabled = False
                stopper.disabled = False
                question_sound.seek(0)
            if answer_sound:
                if answer_sound.state != 'play':
                    answer_player.disabled = False
                stopper.disabled = False
                answer_sound.seek(0)

        def close_popup(btn: Button):
            if question_sound:
                if question_sound.state != 'stop':
                    question_sound.stop()
                # question_sound.unload() todo

            if answer_sound:
                if answer_sound.state != 'stop':
                    answer_sound.stop()
                # answer_sound.unload() todo

            popup.dismiss()

        def add_rating(btn: Button):
            instance.disabled = True
            if self.manager.rating is None:
                raise AssertionError('kek')
            elif len(self.manager.rating) == 0:
                self.manager.teams = set()
                self.manager.teams.add('unknown')
                self.manager.rating = {'unknown': {self.round.get_name(): task.point_count}}
                # raise AssertionError
            else:
                raise AssertionError

        main_layout = GridLayout()
        main_layout.rows = 2
        main_layout.spacing = 10
        main_layout.padding = 10

        label = Label(text=f'{self.round.get_name()}\n{task.category_name}\nКоличество очков : {task.point_count}',
                      **milk_header_style)
        main_layout.add_widget(label)
        popup = Popup(content=main_layout, auto_dismiss=False, title=f'Вопрос')

        layout = BoxLayout(orientation='vertical')
        layout.spacing = 10
        layout.padding = [20, 10]

        question_player = Button(text='Прослушать вопрос', **melody_button_style)
        answer_player = Button(text='Прослушать ответ', **melody_button_style)
        stopper = Button(text='Остановить воспроизведение', **melody_button_style)
        reset = Button(text='Перемотать мелодию в начало', **melody_button_style)
        rating_btn = Button(text='Засчитать рейтинг', **melody_button_style)
        exit_btn = Button(text='Закрыть', **menu_button_style)

        question_player.bind(on_press=lambda x: play_sound(question_sound, x))
        answer_player.bind(on_press=lambda x: play_sound(answer_sound, x))
        stopper.bind(on_press=stop_sound)
        exit_btn.bind(on_press=close_popup)
        reset.bind(on_press=reset_melody)
        rating_btn.bind(on_press=lambda x: self._teams_popup(task.point_count, x))

        layout.add_widget(question_player)
        layout.add_widget(stopper)
        layout.add_widget(reset)
        layout.add_widget(answer_player)
        layout.add_widget(rating_btn)
        layout.add_widget(exit_btn)

        main_layout.add_widget(layout)
        return popup

    def _teams_popup(self, point_count: int, instance: Button):
        instance.disabled = True
        layout = BoxLayout(orientation='vertical')
        popup = Popup(content=layout, auto_dismiss=False, title=f'Выбор команды для начисления рейтинга')
        layout.spacing = 10
        layout.padding = [20, 10]

        def _add_rating(team: str, instance: Button):
            instance.disabled = True
            self.manager.rating[team][self.round.get_name()] = point_count

        for team in self.manager.teams:
            button = Button(text=team, **melody_button_style)
            button.bind(on_press=lambda x: _add_rating(team, x))
            layout.add_widget(button)
        exit_btn = Button(text='Закрыть', **menu_button_style)
        layout.add_widget(exit_btn)
        exit_btn.bind(on_press=popup.dismiss)
        popup.open()
