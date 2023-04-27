"""
My first application
"""
import asyncio
import io
import tempfile
from random import randint

import matplotlib.pyplot as plt
import pyxdf
import toga
from pylsl import *
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

listeString = ["Il est tard mon ami"]


class HelloWorld(toga.App):
    nbGraphes = 0  # number of generated graph
    boucle = True
    tab_val = [0]
    tab_timestamp = [0]

    def createData(self):
        """
        Generate pie chart
        """
        # Create the figure
        plt.figure()
        plt.plot(HelloWorld.tab_timestamp, HelloWorld.tab_val)
        plt.xlabel("nbGraphes")
        plt.ylabel("valeur")
        # Trying to remove the previous graph
        try:
            self.main_box.remove(self.imageChart)
        except:
            pass

        # Save the graph in a temporary file
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        HelloWorld.tab_val = []
        HelloWorld.tab_timestamp = []
        fp = tempfile.NamedTemporaryFile()
        with open(f"{fp.name}.png", 'wb') as f:
            f.write(buf.getvalue())
        self.listeTempFile.append(fp.name)

        HelloWorld.nbGraphes += 1
        plt.close()

    def afficherGraphe(self, widget):
        """
        Display the graph
        """
        # Create the graph
        self.createData()

        # Display the graph
        save = self.listeTempFile[HelloWorld.nbGraphes - 1] + ".png"
        self.image = toga.Image(save)
        self.imageChart = toga.ImageView(id='view1', image=self.image)
        self.main_box.add(self.imageChart)

        # Remove the button
        if HelloWorld.nbGraphes >= 1:
            self.boutonChart.enabled = False
            self.main_box.remove(self.boutonChart)

        # Start the background task
        self.add_background_task(self.regenGraphe)

    async def regenGraphe(self, widget):
        """
        Regenerate the graph every 3 seconds
        """
        await asyncio.sleep(3)
        # Create the graph
        self.createData()

        # Display the graph
        save = self.listeTempFile[HelloWorld.nbGraphes - 1] + ".png"
        self.image = toga.Image(save)
        self.imageChart = toga.ImageView(id='view1', image=self.image)
        self.main_box.add(self.imageChart)

        # Start the background task
        self.add_background_task(self.regenGraphe)

    def startup(self):
        """
        Construct and show the Toga application.
        """
        # Create the main box
        self.main_box = toga.Box(style=Pack(direction=COLUMN))

        # Create the button
        self.boutonChart = toga.Button("Commencer la visualisation", on_press=self.afficherGraphe)
        button = toga.Button(
            "Say Hello!",
            on_press=self.say_hello,
            style=Pack(padding=5)
        )
        self.boutonRecordDonnes = toga.Button("Record", on_press=self.startRecord)

        # Create the label
        self.labelhttpx = toga.Label("False")
        name_label = toga.Label(
            "Your name: ",
            style=Pack(padding=(0, 5))
        )

        # Create the name input
        self.name_input = toga.TextInput(style=Pack(flex=1))
        self.name_input.placeholder = "Test"

        self.listeTempFile = []

        # Create the name box
        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)

        # Add the elements to the main box
        self.main_box.add(self.labelhttpx)
        self.main_box.add(name_box)
        self.main_box.add(button)
        self.main_box.add(self.boutonChart)
        self.main_box.add(self.boutonRecordDonnes)

        # Create the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()

        # Start the background task
        self.add_background_task(self.changeTitle)
        self.add_background_task(self.changeTrueTitle)

        # test XDF
        data, header = pyxdf.load_xdf(
            r"C:\Users\killian\Documents\GitHub\LSLVisualiser\appvisulsl\src\appvisulsl\resources\data.xdf")
        print(data)

        # test LSL
        outlet = StreamInfo(name='myStream', type='EEG', channel_count=8)
        print(outlet)

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

    def startRecord(self, widget):
        print("looking for eeg streams")
        self.streams = resolve_stream('type', 'EEG')
        print('lecture des données')
        self.boutonStop = toga.Button('Stop record', on_press=self.stopRecord)
        self.main_box.add(self.boutonStop)
        self.add_background_task(self.showData)

    def stopRecord(self, widget):
        HelloWorld.boucle = False

    async def showData(self, widget):
        await asyncio.sleep(0.001)
        try:
            self.main_box.remove(self.boutonRecordDonnes)
        except:
            pass
        inlet = stream_inlet(self.streams[0])
        samples,timestamp = inlet.pull_sample()
        for sample in samples:
            HelloWorld.tab_val.append(sample)
            HelloWorld.tab_timestamp.append(timestamp)
        if HelloWorld.boucle:
            self.add_background_task(self.showData)
        else:
            try:
                self.main_box.remove(self.boutonStop)
            except:
                pass
            self.main_box.add(self.boutonRecordDonnes)
            HelloWorld.boucle = True


def greeting(name):
    if name:
        return f"Hello, {name}"
    else:
        return "Hello, stranger"


def main():
    return HelloWorld()
