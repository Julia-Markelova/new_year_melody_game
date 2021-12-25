import json
import traceback
from json import JSONDecodeError
from time import sleep
from typing import Dict
import serial

import vlc
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from config.styles import melody_button_style
from config.styles import menu_button_style
from config.styles import milk_header_style
from tasks.categories import Task


class BtnManager:

    def __init__(
            self,
            answer_sound: vlc.MediaPlayer,
            question_sound: vlc.MediaPlayer,
            task: Task,
            rating: Dict[str, Dict[str, int]],
            round_name: str,
            button_number_to_command_mapping: Dict[int, str],
            task_btn: Button,
            question_player_btn: Button,):

        self.serial_port = None

        self.answer_sound = answer_sound
        self.question_sound = question_sound
        self.task = task
        self.rating = rating
        self.round_name = round_name
        self.task_btn = task_btn
        self.button_number_to_command_mapping = button_number_to_command_mapping
        self.question_player_btn = question_player_btn
        self._finish = True

    def manage_buttons(self):
        self.serial_port = serial.Serial(port='/dev/ttyACM0')
        self.serial_port.reset_input_buffer()
        while not self._finish:
            number = self.get_pressed_button_number()
            if number is not None and self.button_number_to_command_mapping.get(number, None) is not None:
                self._finish = True
                self.on_btn_pressed(self.button_number_to_command_mapping[number])
        self.serial_port.close()

    def get_pressed_button_number(self):
        try:
            for line in self.serial_port:
                line = line.decode('utf-8')
                line = line.replace('\'', '"')
                line = json.loads(line)
                number = int(line['button'])
                return number
        except JSONDecodeError as e:
            print('JSON ERROR', e)
        except Exception as e:
            traceback.print_tb(e)
            print(e)

    def stop(self):
        self._finish = True

    def start(self):
        self._finish = False

    def on_btn_pressed(self, command_name: str):
        self.pause_music()
        popup = self.configure_answer_popup(command_name)
        popup.open()

    def pause_music(self):
        if self.question_sound:
            self.question_sound.pause()
        if self.answer_sound:
            self.answer_sound.pause()

    def configure_answer_popup(self, command_name: str):

        def close_popup(btn: Button):
            self.stop()
            self.question_player_btn.disabled = False
            popup.dismiss()

        def wrong_answer(btn: Button):
            # todo штрафовать за ответ?
            pass
            # self.manage_buttons()

        def add_rating(btn: Button):
            btn.disabled = True
            self.task_btn.disabled = True
            wrong_answer_btn.disabled = True

            if self.rating.get(command_name, None) is not None:
                if self.rating[command_name].get(self.round_name) is None:
                    self.rating[command_name][self.round_name] = 0
                self.rating[command_name][self.round_name] += self.task.point_count

        main_layout = GridLayout()
        main_layout.rows = 2
        main_layout.spacing = 10
        main_layout.padding = 10

        label = Label(
            text=f'Категория "{self.task.category_name}"\n'
                 f'Количество очков : {self.task.point_count}\n\n'
                 f'Отвечает команда {command_name}',
            **milk_header_style)
        main_layout.add_widget(label)
        popup = Popup(content=main_layout, auto_dismiss=False, title=f'Ответ команды {command_name}')

        layout = BoxLayout(orientation='vertical')
        layout.spacing = 10
        layout.padding = [20, 10]

        rating_btn = Button(text='Засчитать рейтинг', **melody_button_style)
        wrong_answer_btn = Button(text='Ответ неверный', **melody_button_style)
        exit_btn = Button(text='Закрыть', **menu_button_style)

        exit_btn.bind(on_press=close_popup)
        wrong_answer_btn.bind(on_press=wrong_answer)
        rating_btn.bind(on_press=add_rating)

        layout.add_widget(rating_btn)
        layout.add_widget(wrong_answer_btn)
        layout.add_widget(exit_btn)

        main_layout.add_widget(layout)
        return popup


if __name__ == '__main__':
    while True:
        try:
            with serial.Serial(port='/dev/ttyACM0') as s:
                sleep(3)
                s.reset_input_buffer()
                for line in s:
                    line = line.decode('utf-8')
                    line = line.replace('\'', '"')
                    line = json.loads(line)
                    number = int(line['button'])
                    print(number)
        except Exception as e:
            print(e)
            pass