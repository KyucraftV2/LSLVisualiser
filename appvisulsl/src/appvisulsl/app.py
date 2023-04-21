"""
My first application
"""
import asyncio
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import matplotlib.pyplot as plt

listeString = ["Il est tard mon ami"]

class HelloWorld(toga.App):

    def createData(self):
        labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
        sizes = [15, 30, 45, 10]
        plt.subplots()
        plt.pie(sizes,labels=labels)
        plt.savefig("temp.png")

    def afficherGraphe(self,widget):
        self.createData()
        image = toga.Image("resources/pieChart.png")
        imageChart = toga.ImageView(id='view1', image=image)
        self.main_box.add(imageChart)
        self.main_window.content = self.main_box
        self.main_window.show()

    def startup(self):

        self.createData()
        self.main_box = toga.Box(style=Pack(direction=COLUMN))
        name_label = toga.Label(
            "Your name: ",
            style=Pack(padding=(0, 5))
        )

        self.boutonChart = toga.Button("Afficher le graphe", on_press=self.afficherGraphe)

        self.labelhttpx = toga.Label("False")

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


        self.main_box.add(self.labelhttpx)
        self.main_box.add(name_box)
        self.main_box.add(button)
        self.main_box.add(self.boutonChart)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
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
