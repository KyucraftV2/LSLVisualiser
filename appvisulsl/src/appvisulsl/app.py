"""
My first application
"""
import asyncio
import io
import tempfile

import matplotlib.pyplot as plt
import toga
from pylsl import *
from toga.style import Pack
from toga.style.pack import COLUMN


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
        if AppLSLVisu.streamChoose:
            placeStream = getStream(AppLSLVisu.tabStreams, self.textInput.value)
            plt.figure()
            plt.plot(AppLSLVisu.tabTimestamp[placeStream], AppLSLVisu.tabVal[placeStream])
            plt.xlabel("timestamp")
            plt.ylabel("value")
            plt.title("Graph of the stream " + AppLSLVisu.tabStreams[placeStream].name())

            try:
                self.boxGraph.clear()
            except:
                pass

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            if AppLSLVisu.nbGraphGenerated % 2 == 0 and len(AppLSLVisu.tabTimestamp[1]) > 2:
                AppLSLVisu.tabVal[placeStream] = AppLSLVisu.tabVal[placeStream][AppLSLVisu.nbValPlot - 2:]
                AppLSLVisu.tabTimestamp[placeStream] = AppLSLVisu.tabTimestamp[placeStream][AppLSLVisu.nbValPlot - 2:]
                AppLSLVisu.nbValPlot = 0
            fp = tempfile.NamedTemporaryFile()
            fp.name = fp.name + AppLSLVisu.tabStreams[placeStream].name()
            with open(f"{fp.name}.png", 'wb') as f:
                f.write(buf.getvalue())
            self.listTempFile.append(fp.name)
            plt.close()
        else:
            for i in range(len(AppLSLVisu.tabStreams)):
                # Create the figure and the plot
                plt.figure()
                plt.plot(AppLSLVisu.tabTimestamp[i], AppLSLVisu.tabVal[i])
                plt.xlabel("timestamp")
                plt.ylabel("value")
                plt.title("Graph of the stream " + AppLSLVisu.tabStreams[i].name())

                # Trying to remove the previous graph
                try:
                    self.listBoxGraph[i].clear()
                except:
                    pass

                # Save the graph in a temporary file
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                if AppLSLVisu.nbGraphGenerated % 2 == 0 and len(AppLSLVisu.tabTimestamp[1]) > 2:
                    AppLSLVisu.tabVal[i] = AppLSLVisu.tabVal[i][AppLSLVisu.nbValPlot - 2:]
                    AppLSLVisu.tabTimestamp[i] = AppLSLVisu.tabTimestamp[i][AppLSLVisu.nbValPlot - 2:]
                    AppLSLVisu.nbValPlot = 0
                fp = tempfile.NamedTemporaryFile()
                fp.name = fp.name + AppLSLVisu.tabStreams[i].name()
                with open(f"{fp.name}.png", 'wb') as f:
                    f.write(buf.getvalue())
                self.listTempFile.append(fp.name)
                plt.close()

        AppLSLVisu.nbGraphGenerated += 1

    def displayGraph(self, widget):
        """
        Display the graph
        """
        # Create the graph
        self.createGraph()

        # Create button
        self.boutonStopChart = toga.Button("Stop generating graph", on_press=self.stopGenerateGraph)
        self.boxButtonGraph.add(self.boutonStopChart)

        if AppLSLVisu.streamChoose:
            save = self.listTempFile[AppLSLVisu.nbGraphGenerated - 1] + ".png"
            self.image = toga.Image(save)
            self.imageGraph = toga.ImageView(image=self.image, id=f"view{AppLSLVisu.countId}")
            self.listImgGraph[0] = self.imageGraph
            self.imageGraph.style.update(width=300, height=300)
            self.boxGraph.add(self.imageGraph)
            AppLSLVisu.countId += 1
        else:
            # Display the graph
            for i in range(len(AppLSLVisu.tabStreams)):
                save = self.listTempFile[AppLSLVisu.nbGraphGenerated - 1 + i] + ".png"
                self.image = toga.Image(save)
                self.imageGraph = toga.ImageView(image=self.image, id=f"view{AppLSLVisu.countId}")
                self.listImgGraph[i] = self.imageGraph
                self.imageGraph.style.update(width=300, height=300)
                self.listBoxGraph[i].add(self.imageGraph)
                AppLSLVisu.countId += 1

        # Remove the button
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

        # Create the graph
        self.createGraph()

        if AppLSLVisu.streamChoose:
            save = self.listTempFile[AppLSLVisu.nbGraphGenerated - 1] + ".png"
            self.image = toga.Image(save)
            self.imageGraph = toga.ImageView(image=self.image, id=f"view{AppLSLVisu.countId}")
            self.imageGraph.style.update(width=300, height=300)
            self.listImgGraph[0] = self.imageGraph
            self.boxGraph.add(self.imageGraph)
            AppLSLVisu.countId += 1
        else:
            # Display the graph
            for i in range(len(AppLSLVisu.tabStreams)):
                save = self.listTempFile[AppLSLVisu.nbGraphGenerated - 1 + i] + ".png"
                self.image = toga.Image(save)
                self.imageGraph = toga.ImageView(image=self.image, id=f"view{AppLSLVisu.countId}")
                self.imageGraph.style.update(width=300, height=300)
                self.listImgGraph[i] = self.imageGraph
                self.listBoxGraph[i].add(self.imageGraph)
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

        # Add the button to the box corresponding
        self.boxButtonGetStream.add(self.buttonGetStream)

        # Add the boxes to the main box
        self.mainBox.add(self.boxButtonGetStream)
        self.mainBox.add(self.boxButtonPreference)
        self.mainBox.add(self.boxButtonGraph)
        self.mainBox.add(self.boxButtonRecord)

        self.scrolling.content = self.mainBox

        # Create the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.scrolling
        self.main_window.show()

    def startRecord(self, widget):
        self.buttonStopRecord = toga.Button('Stop record', on_press=self.stopRecord)
        self.boxButtonRecord.add(self.buttonStopRecord)
        self.add_background_task(self.recordData)

    def stopRecord(self, widget):
        AppLSLVisu.isRecord = False
        self.boxButtonRecord.remove(self.buttonStopRecord)
        self.boxButtonRecord.add(self.buttonRecordData)
        self.boxButtonRecord.refresh()

    def stopGenerateGraph(self, widget):
        AppLSLVisu.isGenerateGraph = False
        self.boxButtonGraph.remove(self.boutonStopChart)
        self.boxButtonGraph.add(self.buttonGraph)
        self.boxButtonGraph.refresh()

    async def recordData(self, widget):
        await asyncio.sleep(0.001)
        try:
            self.boxButtonRecord.remove(self.buttonRecordData)
        except:
            pass
        for i in range(len(AppLSLVisu.tabStreams)):
            inlet = stream_inlet(AppLSLVisu.tabStreams[i])
            samples, timestamp = inlet.pull_sample()
            AppLSLVisu.tabTimestamp[i].append(timestamp)
            AppLSLVisu.tabVal[i].append(samples[0])
        AppLSLVisu.nbValPlot += 1
        if AppLSLVisu.isRecord:
            self.add_background_task(self.recordData)
        else:
            try:
                self.boxButtonRecord.remove(self.buttonStopRecord)
            except:
                pass
                pass
            self.boxButtonRecord.add(self.buttonRecordData)
            AppLSLVisu.isRecord = True

    def getStream(self, widget):
        AppLSLVisu.tabStreams = resolve_streams()
        AppLSLVisu.tabVal = [[0]] * len(AppLSLVisu.tabStreams)
        AppLSLVisu.tabTimestamp = [[0]] * len(AppLSLVisu.tabStreams)
        self.listImgGraph = [0] * len(AppLSLVisu.tabStreams)
        self.boxButtonGraph.add(self.buttonGraph)
        self.boxButtonRecord.add(self.buttonRecordData)
        self.boxButtonPreference.add(self.buttonPreference)
        bigbox = toga.Box(style=Pack(direction=COLUMN))
        for i in range(len(AppLSLVisu.tabStreams)):
            box = toga.Box(style=Pack(direction=COLUMN), id=f"box{i}")
            self.listBoxGraph.append(box)
            self.mainBox.add(box)

    def preference(self, widget):
        self.boxButtonPreference.remove(self.buttonPreference)
        self.textInput = toga.TextInput(id="textInput", placeholder="Enter the name of the stream")
        self.button = toga.Button("Confirm", on_press=self.chooseStream)
        self.back = toga.Button("Back", on_press=self.backPreference)
        self.boxButtonPreference.add(self.textInput)
        self.boxButtonPreference.add(self.button)
        self.boxButtonPreference.add(self.back)

    def chooseStream(self, widget):
        listNameOfStream = [stream.name() for stream in AppLSLVisu.tabStreams]
        listPrint = ""
        for name in listNameOfStream:
            listPrint += "- " + name + "\n"
        if self.textInput.value in listNameOfStream:
            self.main_window.info_dialog("Success", "The stream has been found")
            self.boxButtonPreference.remove(self.textInput)
            self.boxButtonPreference.remove(widget)
            self.boxButtonPreference.remove(self.back)
            self.boxButtonPreference.add(self.buttonPreference)
            AppLSLVisu.streamChoose = True
            self.nameStream = self.textInput.value
            self.listBoxGraph = []
            self.boxGraph = toga.Box()
            self.mainBox.add(self.boxGraph)
        else:
            self.main_window.info_dialog("Error",
                                         f"The stream has not been found, please try again\nList stream :\n{listPrint}")

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
    listName = [stream.name() for stream in listStream]
    return listName.index(nameStream)


def main():
    return AppLSLVisu()
