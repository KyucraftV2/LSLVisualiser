"""
My first application
"""
import asyncio
import os

import matplotlib.pyplot as plt
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

listeString = ["Il est tard mon ami"]


class HelloWorld(toga.App):
    nbGraphes = 0 # number of generated graph
    valeurDict = 1
    dictVal = {1: {
        'labels': ['Frogs', 'Hogs', 'Dogs', 'Logs'],
        'sizes': [35, 9, 19, 37]
    },
        2: {
            'labels': ['Frogs', 'Hogs', 'Dogs', 'Logs'],
            'sizes': [19, 33, 21, 27]
        },
        3: {
            'labels': ['Frogs', 'Hogs', 'Dogs', 'Logs'],
            'sizes': [20, 43, 28, 9]
        },
        4: {
            'labels': ['Frogs', 'Hogs', 'Dogs', 'Logs'],
            'sizes': [23, 5, 22, 50]
        },
        5: {
            'labels': ['Frogs', 'Hogs', 'Dogs', 'Logs'],
            'sizes': [15, 43, 23, 19]
        }}

    def createData(self):
        """
        Generate pie chart
        """
        plt.pie(HelloWorld.dictVal[HelloWorld.valeurDict]['sizes'],
                labels=HelloWorld.dictVal[HelloWorld.valeurDict]['labels'])
        try:
            save = os.path.join(os.path.normpath(toga.App.app.paths.app), str(HelloWorld.nbGraphes) + ".png")
            try:
                self.main_box.remove(self.imageChart)
            except:
                pass
            plt.savefig(save)
            HelloWorld.nbGraphes += 1
            if HelloWorld.valeurDict < 5:
                HelloWorld.valeurDict += 1
            elif HelloWorld.valeurDict == 5:
                HelloWorld.valeurDict = 1
            plt.close()
        except:
            save = os.path.join(os.path.normpath(toga.App.app.paths.app), str(HelloWorld.nbGraphes) + ".png")
            try:
                self.main_box.remove(self.imageChart)
                self.imageChart = None
                self.image = None
            except:
                pass
            plt.savefig(save)
            HelloWorld.nbGraphes += 1
            if HelloWorld.valeurDict < 5:
                HelloWorld.valeurDict += 1
            elif HelloWorld.valeurDict == 5:
                HelloWorld.valeurDict = 1
            plt.close()

    def afficherGraphe(self, widget):
        """
        Display the graph
        """
        self.createData()
        try:
            save = os.path.join(os.path.normpath(toga.App.app.paths.app), str(HelloWorld.nbGraphes - 1) + ".png")
        except:
            save = os.path.join(os.path.normpath(toga.App.app.paths.app), str(HelloWorld.nbGraphes - 1) + ".png")
        self.image = toga.Image(save)
        self.imageChart = toga.ImageView(id='view1', image=self.image)
        self.main_box.add(self.imageChart)
        self.main_window.content = self.main_box
        self.main_window.show()
        # self.add_background_task(self.regenGraphe)

    # def regenGraphe(self,widget):
    #     yield 3
    #     if HelloWorld.valeurDict < 5:
    #         HelloWorld.valeurDict += 1
    #     elif HelloWorld.valeurDict == 5:
    #         HelloWorld.valeurDict = 1
    #     self.createData()
    #     save = os.path.join(os.environ['USERPROFILE'], r'Downloads\test.png')
    #     image = toga.Image(save)
    #     imageChart = toga.ImageView(id='view1', image=image)
    #     self.main_box.add(imageChart)
    #     self.main_window.content = self.main_box
    #     self.main_window.show()
    #     self.add_background_task(self.regenGraphe)

    def startup(self):
        """
        Construct and show the Toga application.
        """
        self.main_box = toga.Box(style=Pack(direction=COLUMN))
        name_label = toga.Label(
            "Your name: ",
            style=Pack(padding=(0, 5))
        )

        self.boutonChart = toga.Button("Afficher le graphe", on_press=self.afficherGraphe)

        self.labelhttpx = toga.Label("False")
        self.listeTempFile = []

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

        buttonQuit = toga.Button(
            "Leave",
            on_press=self.closeTelephone,
            style=Pack(padding=5)
        )

        self.main_box.add(self.labelhttpx)
        self.main_box.add(name_box)
        self.main_box.add(button)
        self.main_box.add(buttonQuit)
        self.main_box.add(self.boutonChart)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()
        self.add_background_task(self.changeTitle)
        self.add_background_task(self.changeTrueTitle)
        self.app.on_exit = self.fermerture

    def say_hello(self, widget):
        """
        Respond to the click of the button by updating the label
        """
        self.main_window.info_dialog(
            greeting(self.name_input.value),
            "Hi there!",
        )

    def changeTitle(self, widget):
        """
        Change the title of the window after 3 seconds
        """
        yield 3
        self.main_window.title = "Il est tard"

    async def changeTrueTitle(self, widget):
        """
        Change again the title of the window after 10 seconds
        """
        await asyncio.sleep(10)
        self.main_window.title = "Il est vraiment tard"

    def fermerture(self, widget):
        """
        Function executing when the app is closing
        """
        print("Au revoir")
        save = os.path.normpath(toga.App.app.paths.app)
        i = 0
        for file in os.listdir(save):
            if (file == str(i) + ".png"):
                os.remove(os.path.join(os.path.normpath(toga.App.app.paths.app), file))
                i += 1
            if i > HelloWorld.nbGraphes:
                break
        return True

    def closeTelephone(self, widget):
        """
        Test function
        """
        print("Au revoir")


def greeting(name):
    if name:
        return f"Hello, {name}"
    else:
        return "Hello, stranger"


def main():
    return HelloWorld()
