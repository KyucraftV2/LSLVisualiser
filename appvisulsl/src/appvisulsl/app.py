"""
My first application
"""
import asyncio
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import httpx

listeString = ["Il est tard mon ami"]

class HelloWorld(toga.App):

    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))
        name_label = toga.Label(
            "Your name: ",
            style=Pack(padding=(0, 5))
        )

        #self.labelnp = toga.Label(np.array([1,2,3,4,5,6,7,8,9]))

        self.labelhttpx = toga.Label(httpx.URL("perdu.com").is_absolute_url)

        self.name_input = toga.TextInput(style=Pack(flex=1))
        self.name_input.placeholder = "Test"

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)

        button = toga.Button(
            "Say Hello!",
            on_press=self.say_hello,
            style=Pack(padding=5)
        )


        main_box.add(self.labelhttpx)
        main_box.add(name_box)
        main_box.add(button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
        self.add_background_task(self.changeTitle)
        self.add_background_task(self.changeTrueTitle)

    def say_hello(self, widget):
        self.main_window.info_dialog(
            greeting(self.name_input.value),
            "Hi there!",
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
