from kivy.app import App  
from kivy.core.window import Window

from widgets import MainWindow, TEAL    


Window.clearcolor = TEAL

class TodoApp(App):
    title = "Todo App"

    def build(self):
        return MainWindow()
    
if __name__ == "__main__":
    todoapp = TodoApp()
    TodoApp().run()