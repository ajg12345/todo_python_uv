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
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
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

    def add_todo_item(self, todo_item):
        if todo_item.isspace() or todo_item == "":
            return
        self.db.add_todo_item(todo_item)
        self.todoitems.clear_widgets()
        self.show_existing_items()
        self.inputframe.todo_input_widget.text = ""

    def mark_as_done(self, item_id):
        for item in self.todoitems.children:
            if item.item_id == item_id:
                self.db.mark_as_done(item_id)
                item.mark_done_button.disabled = True

    def delete_todo_item(self, item_id):
        for item in self.todoitems.children:
            if item.item_id == item_id:
                self.db.delete_todo_item(item_id)
                item.parent.remove_widget(item)        
    
    def show_existing_items(self):
        items = self.db.retrieve_all_items()
        for item in reversed(items):
            item_id, todo_item, done = item
            item = Item(self, item_id, todo_item, done)
            self.todoitems.add_widget(item)
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

    def __init__(self, main_window, **kwargs):
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
        
class Item(BoxLayout):
    size_hint = [1, None]
    spacing = 5

    def __init__(self, main_window, item_id, todo_item, done=False, **kwargs):
        super().__init__(**kwargs)

        self.height = 40
        self.item_id = item_id
        item_display_box = GreenButton(text=todo_item, size_hint=[0.6, 1])

        self.mark_done_button = YellowButton(
            text="Done", size_hint=[None, 1], width=100, disabled=done
        )
        self.mark_done_button.bind(
            on_release=lambda *args: main_window.mark_as_done(item_id)
        )

        remove_button = YellowButton(
            text="-",
            size_hint=[None, 1], 
            width=40
        )
        remove_button.bind(
            on_release=lambda *args: main_window.delete_todo_item(item_id)
        )

        self.add_widget(item_display_box)
        self.add_widget(self.mark_done_button)
        self.add_widget(remove_button)