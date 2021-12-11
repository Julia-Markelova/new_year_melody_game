from typing import List

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.utils import escape_markup

from config.styles import header_style
from config.styles import menu_button_style

from config.styles import round_category_button_style
from config.styles import round_task_button_style
from tasks.categories import Category


class RoundScreen(Screen):
    def __init__(self, categories: List[Category], rating = None, **kwargs):
        super().__init__(**kwargs)
        self.categories = categories
        self.rating = rating
        box_layout = BoxLayout(orientation='vertical')
        box_layout.padding = 10
        box_layout.spacing = 10
        title = Label(text=self.name, **header_style, size_hint=(1, 0.1), size=(100, 30),)
        close_btn = Button(text='Завершить раунд', **menu_button_style, size_hint=(1, 0.1), size=(100, 30), )
        close_btn.bind(on_press=self.finish_round)
        layout = GridLayout()
        self._configure_round_layout(layout)
        box_layout.add_widget(title)
        box_layout.add_widget(layout)
        box_layout.add_widget(close_btn)
        self.add_widget(box_layout)

    def finish_round(self, instance: Button):
        self.rating = 100  # todo
        self.manager.transition.direction = 'right'
        self.manager.current = 'Main Screen'

    def on_btn_pressed(self, instance: Button):
        instance.disabled = True
        content = Button(text='Close me!', size=(300, 80),
                         size_hint=(None, None))
        popup = Popup(content=content, auto_dismiss=False)
        content.bind(on_press=popup.dismiss)
        popup.open()

    def _configure_round_layout(self, layout: GridLayout):
        layout.padding = 0
        layout.spacing = 2
        layout.cols = len(self.categories[0].tasks) + 1
        layout.rows = len(self.categories)

        for category in self.categories:
            layout.add_widget(Button(text=category.name, **round_category_button_style))

            for task in category.tasks:
                button = Button(text=str(task.point_count), **round_task_button_style)
                button.bind(on_press=self.on_btn_pressed if task.handler is None else task.handler)
                layout.add_widget(button)
