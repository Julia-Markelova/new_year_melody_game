from threading import Thread
from time import sleep
from typing import List

import vlc
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
from tasks.button_holder import BtnManager
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
        close_btn = Button(text='В главное меню', **menu_button_style, size_hint=(1, 0.1), size=(100, 30), )
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
            sleep(0.05)
            popup.open()

        return handler

    def _configure_default_popup(self, task: Task, instance: Button) -> Popup:
        question_sound: vlc.MediaPlayer = vlc.MediaPlayer(task.path_to_question)
        answer_sound = None
        if task.path_to_answer is not None:
            answer_sound = vlc.MediaPlayer(task.path_to_answer)

        def play_question(btn: Button):
            if question_sound:
                question_player.disabled = True
                answer_player.disabled = True
                btn_manager.start()
                t = Thread(target=btn_manager.manage_buttons, daemon=True)
                t.start()
                question_sound.play()

        def play_sound(sound: vlc.MediaPlayer, btn: Button):
            if sound:
                btn_manager.stop()
                answer_player.disabled = True
                question_player.disabled = True
                sound.play()

        def stop_sound(btn: Button):
            question_player.disabled = False
            answer_player.disabled = False if task.path_to_answer is not None else True

            if question_sound and question_sound.can_pause() and question_sound.get_state() == vlc.State.Playing:
                question_sound.pause()
            if answer_sound and answer_sound.can_pause() and answer_sound.get_state() == vlc.State.Playing:
                answer_sound.pause()

        def reset_melody(btn: Button):
            if question_sound:
                if question_sound.get_state() == vlc.State.Playing:
                    question_sound.pause()
                question_player.disabled = False
                question_sound.set_position(0)
            if answer_sound:
                if answer_sound.get_state() != vlc.State.Playing:
                    answer_sound.pause()
                answer_player.disabled = False
                answer_sound.set_position(0)

        def close_popup(btn: Button):
            if question_sound:
                if question_sound.get_state() != vlc.State.Stopped:
                    question_sound.stop()

            if answer_sound:
                if answer_sound.get_state != vlc.State.Stopped:
                    answer_sound.stop()
            btn_manager.stop()
            btn_manager.close()
            popup.dismiss()

        def show_answer(btn: Button):
            popup = Popup(content=Label(text=task.answer, **milk_header_style), auto_dismiss=True, title=f'Ответ')
            popup.open()

        main_layout = GridLayout()
        main_layout.rows = 2
        main_layout.spacing = 10
        main_layout.padding = 10

        label = Label(text=f'{self.round.get_name()}\nКатегория "{task.category_name}"\nКоличество очков : {task.point_count}',
                      **milk_header_style)
        main_layout.add_widget(label)
        popup = Popup(content=main_layout, auto_dismiss=False, title=f'Вопрос')

        layout = BoxLayout(orientation='vertical')
        layout.spacing = 10
        layout.padding = [20, 10]

        question_player = Button(text='Прослушать вопрос', **melody_button_style)
        answer_player = Button(text='Прослушать ответ', **melody_button_style, disabled=task.path_to_answer is None)
        stopper = Button(text='Остановить воспроизведение', **melody_button_style)
        reset = Button(text='Перемотать мелодию в начало', **melody_button_style)
        answer = Button(text='Показать ответ', **melody_button_style)
        rating_btn = Button(text='Засчитать рейтинг', **melody_button_style)
        exit_btn = Button(text='Закрыть', **menu_button_style)

        question_player.bind(on_press=play_question)
        answer_player.bind(on_press=lambda x: play_sound(answer_sound, x))
        stopper.bind(on_press=stop_sound)
        exit_btn.bind(on_press=close_popup)
        answer.bind(on_press=show_answer)
        reset.bind(on_press=reset_melody)
        rating_btn.bind(on_press=lambda x: self._teams_popup(task.point_count, instance, x))

        layout.add_widget(question_player)
        layout.add_widget(stopper)
        layout.add_widget(reset)
        layout.add_widget(answer_player)
        layout.add_widget(answer)
        layout.add_widget(rating_btn)
        layout.add_widget(exit_btn)

        main_layout.add_widget(layout)

        btn_manager = self._create_button_manager(
            answer_sound, question_sound, task,
            buttons_to_disable=[instance, rating_btn],
            buttons_to_enable=[question_player, stopper, reset] + ([answer_player] if task.path_to_answer is not None else []))
        return popup

    def _teams_popup(self, point_count: int, task_btn: Button, instance: Button):
        main_layout = GridLayout()
        main_layout.rows = 2
        main_layout.spacing = 10
        main_layout.padding = 10
        layout = BoxLayout(orientation='vertical')
        popup = Popup(content=main_layout, auto_dismiss=False, title=f'Выбор команды для начисления рейтинга')

        layout.spacing = 10
        layout.padding = [30, 30]
        label = Label(text=f'Укажите команду для начисления очков', **milk_header_style, )
        main_layout.add_widget(label)

        def _add_rating(btn: Button):
            instance.disabled = True
            task_btn.disabled = True
            if self.manager.rating.get(btn.text, None) is not None:
                if self.manager.rating[btn.text].get(self.round.get_name()) is None:
                    self.manager.rating[btn.text][self.round.get_name()] = 0
                self.manager.rating[btn.text][self.round.get_name()] += point_count
            for btn in buttons:
                btn.disabled = True

        buttons = []
        for _, team in self.manager.teams.items():
            button = Button(text=team, **melody_button_style)
            button.bind(on_press=_add_rating)
            buttons.append(button)
            layout.add_widget(button)
        fake_team = Button(text='Не засчитывать никому', **melody_button_style)
        fake_team.bind(on_press=_add_rating)
        buttons.append(fake_team)
        layout.add_widget(fake_team)
        exit_btn = Button(text='Закрыть', **menu_button_style)
        layout.add_widget(exit_btn)
        main_layout.add_widget(layout)
        exit_btn.bind(on_press=popup.dismiss)
        popup.open()

    def _create_button_manager(
            self,
            answer_sound: vlc.MediaPlayer,
            question_sound: vlc.MediaPlayer,
            task: Task,
            buttons_to_disable: List[Button],
            buttons_to_enable: List[Button],
):
        btn_manager = BtnManager(
            answer_sound,
            question_sound,
            task,
            self.manager.rating,
            self.manager.stats,
            self.round.get_name(),
            self.manager.teams,
            buttons_to_disable,
            buttons_to_enable
        )
        return btn_manager
