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


class HelloWorld(toga.App):
    nbGraphes = 0  # number of generated graph
    isRecord = True
    isGenerateGraph = False
    tab_val = [0]
    tab_timestamp = [0]
    nbValeurPlot = 0

    def createData(self):
        """
        Generate pie chart
        """
        # Create the figure
        plt.figure()

        plt.plot(HelloWorld.tab_timestamp, HelloWorld.tab_val)
        plt.xlabel("timestamp")
        plt.ylabel("value")
        # Trying to remove the previous graph
        try:
            self.main_box.remove(self.imageChart)
        except:
            pass

        # Save the graph in a temporary file
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        HelloWorld.tab_val = HelloWorld.tab_val[HelloWorld.nbValeurPlot-2:]
        HelloWorld.tab_timestamp = HelloWorld.tab_timestamp[HelloWorld.nbValeurPlot-2:]
        HelloWorld.nbValeurPlot = 0
        fp = tempfile.NamedTemporaryFile()
        with open(f"{fp.name}.png", 'wb') as f:
            f.write(buf.getvalue())
        self.listeTempFile.append(fp.name)

        HelloWorld.nbGraphes += 1
        plt.close()

    def displayGraph(self, widget):
        """
        Display the graph
        """
        # Create the graph
        self.createData()

        # Create button
        self.boutonStopChart = toga.Button("Stop generating graph", on_press=self.stopGenerateGraph)
        self.main_box.add(self.boutonStopChart)

        # Display the graph
        save = self.listeTempFile[HelloWorld.nbGraphes - 1] + ".png"
        self.image = toga.Image(save)
        self.imageChart = toga.ImageView(id='view1', image=self.image)
        self.main_box.add(self.imageChart)

        # Remove the button
        if HelloWorld.nbGraphes >= 1:
            self.main_box.remove(self.boutonChart)

        # Start the background task
        self.add_background_task(self.regenGraph)
        HelloWorld.isGenerateGraph = True

    async def regenGraph(self, widget):
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
        if HelloWorld.isGenerateGraph:
            self.add_background_task(self.regenGraph)

    def startup(self):
        """
        Construct and show the Toga application.
        """
        # Create the main box
        self.main_box = toga.Box(style=Pack(direction=COLUMN))

        # Create the button
        self.boutonChart = toga.Button("Start visualisation", on_press=self.displayGraph)
        self.boutonRecordDonnes = toga.Button("Starting recording LSL", on_press=self.startRecord)

        # Create the list of temporary files
        self.listeTempFile = []

        # Add the elements to the main box
        self.main_box.add(self.boutonChart)
        self.main_box.add(self.boutonRecordDonnes)

        # Create the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()

    def startRecord(self, widget):
        self.main_window.info_dialog("Searching for LSL streams","Searching in progress")
        self.streams = resolve_stream('type', 'EEG')
        self.boutonStop = toga.Button('Stop record', on_press=self.stopRecord)
        self.main_box.add(self.boutonStop)
        self.add_background_task(self.recordData)

    def stopRecord(self, widget):
        HelloWorld.isRecord = False
        self.main_box.remove(self.boutonStop)
        self.main_box.add(self.boutonRecordDonnes)
        self.main_window.show()

    def stopGenerateGraph(self, widget):
        HelloWorld.isGenerateGraph = False
        self.main_box.remove(self.boutonStopChart)
        self.main_box.add(self.boutonChart)
        self.main_window.show()

    async def recordData(self, widget):
        await asyncio.sleep(0.001)
        try:
            self.main_box.remove(self.boutonRecordDonnes)
        except:
            pass
        inlet = stream_inlet(self.streams[0])
        samples, timestamp = inlet.pull_sample()
        HelloWorld.tab_timestamp.append(timestamp)
        HelloWorld.tab_val.append(samples[0])
        HelloWorld.nbValeurPlot += 1

        # for sample in samples:
        #     HelloWorld.tab_val.append(sample)
        #     HelloWorld.tab_timestamp.append(timestamp)
        if HelloWorld.isRecord:
            self.add_background_task(self.recordData)
        else:
            try:
                self.main_box.remove(self.boutonStop)
            except:
                pass
            self.main_box.add(self.boutonRecordDonnes)
            HelloWorld.isRecord = True


def main():
    return HelloWorld()
