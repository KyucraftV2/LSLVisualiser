"""
My first application
"""
import asyncio

#briefcase run android -d "@Pixel_3a_API_33_x86_64"
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import httpx


class HelloWorld(toga.App):

    def startup(self):
        self.text_appearance = True
        main_box = toga.Box(style=Pack(direction=COLUMN))

        name_label = toga.Label(
            "Your name: ",
            style=Pack(padding=(0, 5))
        )

        self.name_input = toga.TextInput(style=Pack(flex=1))

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)

        button = toga.Button(
            "Say Hello!",
            on_press=self.say_hello,
            style=Pack(padding=5)
        )

        main_box.add(name_box)
        main_box.add(button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
        self.add_background_task(self.changeTitle)
        self.add_background_task(self.changeTrueTitle)

    def say_hello(self, widget):
        with httpx.Client() as client:
            response = client.get("https://jsonplaceholder.typicode.com/posts/42")

        payload = response.json()

        self.main_window.info_dialog(
            greeting(self.name_input.value),
            payload["body"],
        )

    def changeTitle(self,widget):
        yield 3
        self.main_window.title = "Il est tard"

    async def changeTrueTitle(self,widget):
        await asyncio.sleep(10)
        self.main_window.title = "Il est vraiment tard"

def greeting(name):
    if name:
        return f"Hello, {name}"
    else:
        return "Hello, stranger"


def main():
    return HelloWorld()
