from kivy.core.audio import Sound
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup


def handle_a_100(instance: Button):
    instance.disabled = True
    path_to_melody = 'melodies/Adele — Rolling In The Deep.mp3'
    task_name = 'A 100'
    popup = _configure_popup(task_name, path_to_melody)
    popup.open()


def handle_a_200(instance: Button):
    instance.disabled = True
    path_to_melody = 'melodies/Lana Del Rey — Summertime Sadness.mp3'
    task_name = 'A 200'
    popup = _configure_popup(task_name, path_to_melody)
    popup.open()


def _configure_popup(task_name: str, path_to_melody: str) -> Popup:
    sound: Sound = SoundLoader.load(path_to_melody)

    def play_melody(btn: Button):
        if sound:
            btn.disabled = True
            stopper.disabled = False
            sound.play()
        else:
            print('No melody found')

    def stop_melody(btn: Button):
        if sound:
            btn.disabled = True
            player.disabled = False
            sound.stop()

    def reset_melody(btn: Button):
        if sound:
            if sound.state != 'play':
                player.disabled = False
            stopper.disabled = False
            sound.seek(0)

    def close_popup(btn: Button):
        if sound:
            sound.stop()
            sound.unload()
        popup.dismiss()

    layout = BoxLayout(orientation='vertical')
    layout.spacing = 10
    layout.padding = [20, 10]
    popup = Popup(content=layout, auto_dismiss=False)

    label = Label(text=task_name)
    player = Button(text='Play')
    player.bind(on_press=play_melody)
    stopper = Button(text='Stop')
    stopper.bind(on_press=stop_melody)
    exit = Button(text='Finish')
    exit.bind(on_press=close_popup)
    reset = Button(text='Reset')
    reset.bind(on_press=reset_melody)

    layout.add_widget(label)
    layout.add_widget(player)
    layout.add_widget(stopper)
    layout.add_widget(reset)
    layout.add_widget(exit)

    return popup
