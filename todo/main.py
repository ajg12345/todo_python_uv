from kivy.app import App  
from kivy.core.window import Window
from kivy.logger import Logger, LOG_LEVELS

from database import Database
from widgets import MainWindow, TEAL    

Window.clearcolor = TEAL

class TodoApp(App):
    title = "Todo App"

    def build(self):
        return MainWindow(db=Database())
    
if __name__ == "__main__":
    todoapp = TodoApp()
    TodoApp().run()