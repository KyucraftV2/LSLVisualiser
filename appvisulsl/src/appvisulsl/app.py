"""
My first application
"""
import asyncio
import io
import random
import tempfile

import matplotlib.pyplot as plt
import toga
# from pylsl import *
from toga.style import Pack
from toga.style.pack import COLUMN,ROW


class AppLSLVisu(toga.App):
    nbGraphGenerated = 0  # number of generated graph
    isRecord = True
    isGenerateGraph = False
    tabVal = [0]
    tabTimestamp = [0]
    nbValPlot = 0
    tabStreams = []
    countId = 0
    streamChoose = False

    def createGraph(self):
        """
        Generate data
        """
        for i in range(3):
            print(f"creation du graphe : {i}")
            listeVal = [random.randint(0, 100) for i in range(0, 15)]
            listeTime = [i for i in range(0, 15)]
            plt.figure()
            plt.plot(listeTime, listeVal)
            plt.xlabel("temps")
            plt.ylabel("val")
            plt.title(f"graphe{i}")
            try:
                self.listBoxGraph[i].clear()
            except:
                pass

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            fp = tempfile.NamedTemporaryFile()
            fp.name = fp.name + f"{i}"
            with open(f"{fp.name}.png", 'wb') as f:
                f.write(buf.getvalue())

            self.listTempFile.append(fp.name)
            plt.close()

        AppLSLVisu.nbGraphGenerated += 1

    def displayGraph(self, widget):
        """
        Display the graph
        """
        self.createGraph()
        self.boutonStopChart = toga.Button("Stop generating graph", on_press=self.stopGenerateGraph)
        self.boxButtonGraph.add(self.boutonStopChart)
        for i in range(3):
            save = self.listTempFile[AppLSLVisu.nbGraphGenerated - 1 + i] + ".png"
            self.image = toga.Image(save)
            self.imageGraph = toga.ImageView(image=self.image, id=f"view{AppLSLVisu.countId}")
            size = self.main_window.size
            self.imageGraph.style.update(width=size[0] * 30 / 100, height=size[0] * 30 / 100)
            self.listBoxGraph[i].add(self.imageGraph)
            self.scrolling.refresh()

            AppLSLVisu.countId += 1

        if AppLSLVisu.nbGraphGenerated >= 1:
            self.boxButtonGraph.remove(self.buttonGraph)
        # Start the background task
        self.add_background_task(self.regenGraph)
        AppLSLVisu.isGenerateGraph = True

    async def regenGraph(self, widget):
        """
        Regenerate the graph every 3 seconds
        """
        await asyncio.sleep(3)
        self.createGraph()
        for i in range(3):
            save = self.listTempFile[AppLSLVisu.nbGraphGenerated - 1 + i] + ".png"
            self.image = toga.Image(save)
            self.imageGraph = toga.ImageView(image=self.image, id=f"view{AppLSLVisu.countId}")
            size = self.main_window.size
            self.imageGraph.style.update(width=size[0] * 30 / 100, height=size[0] * 30 / 100)
            self.listBoxGraph[i].add(self.imageGraph)
            print(f"graphe regen : {i}")
            AppLSLVisu.countId += 1

        # Start the background task
        if AppLSLVisu.isGenerateGraph:
            self.add_background_task(self.regenGraph)

    def startup(self):
        """
        Construct and show the Toga application.
        """
        # Create boxes
        self.mainBox = toga.Box(style=Pack(direction=COLUMN))
        self.boxButtonGraph = toga.Box(style=Pack(direction=COLUMN))
        self.boxButtonRecord = toga.Box(style=Pack(direction=COLUMN))
        self.boxButtonGetStream = toga.Box(style=Pack(direction=COLUMN))
        self.boxButtonPreference = toga.Box(style=Pack(direction=COLUMN))

        # Create the button
        self.buttonGraph = toga.Button("Start visualisation", on_press=self.displayGraph)
        self.buttonRecordData = toga.Button("Starting recording LSL", on_press=self.startRecord)
        self.buttonGetStream = toga.Button("Get all LSL streams", on_press=self.getStream)
        self.buttonPreference = toga.Button("Preference", on_press=self.preference)

        # Create the list of temporary files
        self.listTempFile = []

        # Create the list of images
        self.listImgGraph = []

        # Create the list of box for the graph images
        self.listBoxGraph = []

        # Create a scroller for graph
        self.scrolling = toga.ScrollContainer(style=Pack(direction=COLUMN))

        self.bigBoxGraph = toga.Box(style=Pack(direction=COLUMN))

        # Add the button to the box corresponding
        self.boxButtonGetStream.add(self.buttonGetStream)

        #Testing for set two buttons
        b1 = toga.Button("hi",on_press=lambda : print("hi"))
        b2 = toga.Button("hola",on_press=lambda:print("hola"))
        b3 = toga.Button("bonjour", on_press=lambda: print("bonjour"))
        b4 = toga.Button("hallo", on_press=lambda: print("hallo"))

        split = toga.Box(style=Pack(direction=ROW))
        split.add(b1)
        split.add(b2)
        split.add(b3)
        split.add(b4)


        # Add the boxes to the main box
        self.mainBox.add(self.boxButtonGetStream)
        self.mainBox.add(self.boxButtonPreference)
        self.mainBox.add(self.boxButtonGraph)
        self.mainBox.add(self.boxButtonRecord)
        self.mainBox.add(split)

        self.scrolling.content = self.bigBoxGraph

        self.mainBox.add(self.scrolling)

        # Create the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.mainBox
        self.main_window.show()

    def startRecord(self, widget):
        """
        Add task in background with add and remove button
        """
        self.buttonStopRecord = toga.Button('Stop record', on_press=self.stopRecord)
        self.boxButtonRecord.add(self.buttonStopRecord)
        self.add_background_task(self.recordData)

    def stopRecord(self, widget):
        """
        Stop the record with remove and add button
        """
        AppLSLVisu.isRecord = False
        self.boxButtonRecord.remove(self.buttonStopRecord)
        self.boxButtonRecord.add(self.buttonRecordData)
        self.boxButtonRecord.refresh()

    def stopGenerateGraph(self, widget):
        """
        Stop generate graph and remove/add button
        """
        AppLSLVisu.isGenerateGraph = False
        self.boxButtonGraph.remove(self.boutonStopChart)
        self.boxButtonGraph.add(self.buttonGraph)
        self.boxButtonGraph.refresh()

    async def recordData(self, widget):
        """
        Record data with streams LSL
        """
        await asyncio.sleep(0.001)
        pass

    def getStream(self, widget):
        """
        Get all streams and add all button for start record, generate graph etc.
        """
        self.boxButtonGraph.add(self.buttonGraph)
        self.boxButtonRecord.add(self.buttonRecordData)
        self.boxButtonPreference.add(self.buttonPreference)
        for i in range(3):
            box = toga.Box(style=Pack(direction=COLUMN), id=f"box{i}")
            self.listBoxGraph.append(box)
            self.bigBoxGraph.add(box)

    def preference(self, widget):
        """
        For setting just one stream who is generated
        """
        self.boxButtonPreference.remove(self.buttonPreference)
        self.textInput = toga.TextInput(id="textInput", placeholder="Enter the name of the stream")
        self.button = toga.Button("Confirm", on_press=self.chooseStream)
        self.back = toga.Button("Back", on_press=self.backPreference)
        self.boxButtonPreference.add(self.textInput)
        self.boxButtonPreference.add(self.button)
        self.boxButtonPreference.add(self.back)

    def chooseStream(self, widget):
        """
        Method who makes all change when a stream is choose
        """
        pass

    def backPreference(self, widget):
        self.boxButtonPreference.remove(self.textInput)
        self.boxButtonPreference.remove(self.button)
        self.boxButtonPreference.remove(self.back)
        self.boxButtonPreference.add(self.buttonPreference)


def getStream(listStream: list, nameStream: str):
    """
    :param listStream: list of LSL Streams
    :param nameStream: String of name in list
    :return : The place of the stream with the name in parameters
    """
    pass

def main():
    return AppLSLVisu()
