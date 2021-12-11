from kivy.core.audio import Sound
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from config.paths import MELODIES_PATH
from config.styles import melody_button_style
from config.styles import menu_button_style
from config.styles import milk_header_style

QUESTION_NAME = 'question.mp3'
ANSWER_NAME = 'answer.mp3'


def default_handler(round_ind: int, category_name: str, task_name: str):
    def handler(instance: Button):
        instance.disabled = True
        popup = _configure_default_popup(round_ind, category_name, task_name)
        popup.open()
    return handler


def _configure_default_popup(round_ind: int, category_name: str, task_name: str) -> Popup:
    round_name = f'Раунд {round_ind}'
    path_to_question = f'{MELODIES_PATH}/{round_ind}/{category_name}/{task_name}/{QUESTION_NAME}'
    path_to_answer = f'{MELODIES_PATH}/{round_ind}/{category_name}/{task_name}/{ANSWER_NAME}'
    question_sound: Sound = SoundLoader.load(path_to_question)
    answer_sound: Sound = SoundLoader.load(path_to_answer)

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
        # if question_sound:
        #     if question_sound.state != 'stop':
        #         question_sound.stop()
        #     question_sound.unload()
        # if answer_sound:
        #     if answer_sound.state != 'stop':
        #         answer_sound.stop()
        #     answer_sound.unload()
        popup.dismiss()

    main_layout = GridLayout()
    main_layout.rows = 2
    main_layout.spacing = 10
    main_layout.padding = 10

    label = Label(text=f'{round_name}\n{category_name}\nКоличество очков : {task_name}', **milk_header_style)
    main_layout.add_widget(label)
    popup = Popup(content=main_layout, auto_dismiss=False, title=f'Вопрос')

    layout = BoxLayout(orientation='vertical')
    layout.spacing = 10
    layout.padding = [20, 10]

    question_player = Button(text='Прослушать вопрос', **melody_button_style)
    answer_player = Button(text='Прослушать ответ', **melody_button_style)
    stopper = Button(text='Остановить воспроизведение', **melody_button_style)
    reset = Button(text='Перемотать мелодию в начало', **melody_button_style)
    exit_btn = Button(text='Закрыть', **menu_button_style)

    question_player.bind(on_press=lambda x: play_sound(question_sound, x))
    answer_player.bind(on_press=lambda x: play_sound(answer_sound, x))
    stopper.bind(on_press=stop_sound)
    exit_btn.bind(on_press=close_popup)
    reset.bind(on_press=reset_melody)

    layout.add_widget(question_player)
    layout.add_widget(stopper)
    layout.add_widget(reset)
    layout.add_widget(answer_player)
    layout.add_widget(exit_btn)

    main_layout.add_widget(layout)
    return popup