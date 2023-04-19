"""
My first application
"""
import numpy as np
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import numpy as np


class HelloWorld(toga.App):

    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))

        name_label = toga.Label(
            "Your name: ",
            style=Pack(padding=(0, 5))
        )

        chaine = toga.Label(np.array([0,1,2,3,4,5,6,7,8,9]))
        self.name_input = toga.TextInput(style=Pack(flex=1))

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)

        button = toga.Button(
            "Say Hello!",
            on_press=self.say_hello,
            style=Pack(padding=5)
        )

        main_box.add(chaine)
        main_box.add(name_box)
        main_box.add(button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def say_hello(self, widget):
        self.main_window.info_dialog(
            greeting(self.name_input.value),
            "Hi there!",
        )

def greeting(name):
    if name:
        return f"Hello, {name}"
    else:
        return "Hello, stranger"


def main():
    return HelloWorld()
