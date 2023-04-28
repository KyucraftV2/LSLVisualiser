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

    def createGraph(self):
        """
        Generate data
        """
        for i in range(len(AppLSLVisu.tabStreams)):
            # Create the figure and the plot
            plt.figure()
            plt.plot(AppLSLVisu.tabTimestamp[i], AppLSLVisu.tabVal[i])
            plt.xlabel("timestamp")
            plt.ylabel("value")
            plt.title("Graph of the stream " + AppLSLVisu.tabStreams[i].name())

            # Trying to remove the previous graph
            try:
                for graph in self.listImgGraph:
                    self.mainBox.remove(graph)
            except:
                pass

            # Save the graph in a temporary file
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            if AppLSLVisu.nbGraphGenerated % 2 == 0  and len(AppLSLVisu.tabTimestamp[1]) > 2:
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

        # Display the graph
        for i in range(len(AppLSLVisu.tabStreams)):
            save = self.listTempFile[AppLSLVisu.nbGraphGenerated - 1] + ".png"
            self.image = toga.Image(save)
            self.imageGraph = toga.ImageView(id=f'view{i + 1}', image=self.image)
            self.listImgGraph[i] = self.imageGraph

        for graph in self.listImgGraph:
            self.mainBox.add(graph)

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

        # Display the graph
        for i in range(len(AppLSLVisu.tabStreams)):
            save = self.listTempFile[AppLSLVisu.nbGraphGenerated - 1] + ".png"
            self.image = toga.Image(save)
            self.imageGraph = toga.ImageView(id=f'view{i + 1}', image=self.image)
            self.listImgGraph[i] = self.imageGraph

        for graph in self.listImgGraph:
            self.mainBox.add(graph)

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

        # Create the button
        self.buttonGraph = toga.Button("Start visualisation", on_press=self.displayGraph)
        self.buttonRecordData = toga.Button("Starting recording LSL", on_press=self.startRecord)
        self.buttonGetStream = toga.Button("Get LSL streams", on_press=self.getStream)

        # Create the list of temporary files
        self.listTempFile = []

        # Create the list of images
        self.listImgGraph = []

        # Add the button to the box corresponding
        self.boxButtonGetStream.add(self.buttonGetStream)

        # Add the boxes to the main box
        self.mainBox.add(self.boxButtonGetStream)
        self.mainBox.add(self.boxButtonGraph)
        self.mainBox.add(self.boxButtonRecord)

        # Create the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.mainBox
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


def main():
    return AppLSLVisu()
