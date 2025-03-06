from kivy.effects.scroll import ScrollEffect
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

TEAL = (0, 0.31, 0.31, 1.0)
YELLOW = (1.0, 0.85, 0, 1.0)
GREEN = (0.0, 1.0, 0.0, 1.0)

class MainWindow(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        todo_list_container = BoxLayout(
            orientation="vertical",
            size_hint=[.85, None],
            height=350,
            pos_hint={"center_x": 0.5, "top": 0.85},
            spacing=10
        )
        title_label = Label(
            font_size=35,
            text="[b]Todo App[/b]",
            size_hint=[1, None],
            markup=True
        )
        self.inputframe = InputFrame(self)
        self.scrollablelist = ScrollableList()
        self.todoitems = self.scrollablelist.todoitems
        
        todo_list_container.add_widget(title_label)
        todo_list_container.add_widget(self.inputframe)
        todo_list_container.add_widget(self.scrollablelist)

        self.add_widget(todo_list_container)
        
class Input(TextInput):
    max_length = 65
    multiline = False

    def insert_text(self, *args):
        if len(self.text) < self.max_length:
            super().insert_text(*args)

class NoBackgroundButton(Button):
    background_down = ""
    background_normal = ""
    background_disabled = ""

class YellowButton(NoBackgroundButton):
    background_color = YELLOW
    color = TEAL

class GreenButton(NoBackgroundButton):
    background_color = GREEN
    
class InputFrame(BoxLayout):
    spacing = 8
    height = 45
    size_hint_y = None

    def __call__(self, main_window, **kwargs):
        super().__init__(**kwargs)

        self.todo_input_widget = Input(
            hint_text="Enter a todo activity",
            font_size=22
        )
        self.todo_input_widget.padding = [10, 10, 10, 10]
        add_item_button = YellowButton(
            width=self.height,
            size_hint=[None, 1], text="+"
        )
        add_item_button.bind(
            on_release=lambda *args: main_window.add_todo_item(
                self.todo_input_widget.text
            )
        )

        self.add_widget(self.todo_input_widget)
        self.add_widget(add_item_button)


class ScrollableList(ScrollView):
    effect_cls = ScrollEffect

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.height = 400
        self.todoitems = BoxLayout(
            orientation="vertical",
            size_hint_y = None,
            spacing=14
        )

    def adjust_height(self, *args):
        ITEM_HEIGHT = 40
        SPACING = 14
        self.todoitems.height = (ITEM_HEIGHT + SPACING) * (
            len(self.todoitems.children)
        ) - SPACING