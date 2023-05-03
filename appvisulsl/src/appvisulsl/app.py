"""
My first application
"""
import asyncio
import os.path

import toga
# from pylsl import *
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
        pass
        # if AppLSLVisu.streamChoose:
        #     placeStream = getStream(AppLSLVisu.tabStreams, self.textInput.value)
        #     plt.figure()
        #     plt.plot(AppLSLVisu.tabTimestamp[placeStream], AppLSLVisu.tabVal[placeStream])
        #     plt.xlabel("timestamp")
        #     plt.ylabel("value")
        #     plt.title("Graph of the stream " + AppLSLVisu.tabStreams[placeStream].name())
        #
        #     try:
        #         self.boxGraph.clear()
        #     except:
        #         pass
        #
        #     buf = io.BytesIO()
        #     plt.savefig(buf, format='png')
        #     if AppLSLVisu.nbGraphGenerated % 2 == 0 and len(AppLSLVisu.tabTimestamp[1]) > 2:
        #         AppLSLVisu.tabVal[placeStream] = AppLSLVisu.tabVal[placeStream][AppLSLVisu.nbValPlot - 2:]
        #         AppLSLVisu.tabTimestamp[placeStream] = AppLSLVisu.tabTimestamp[placeStream][AppLSLVisu.nbValPlot - 2:]
        #         AppLSLVisu.nbValPlot = 0
        #     fp = tempfile.NamedTemporaryFile()
        #     fp.name = fp.name + AppLSLVisu.tabStreams[placeStream].name()
        #     with open(f"{fp.name}.png", 'wb') as f:
        #         f.write(buf.getvalue())
        #     self.listTempFile.append(fp.name)
        #     plt.close()
        # else:
        #     for i in range(len(AppLSLVisu.tabStreams)):
        #         # Create the figure and the plot
        #         plt.figure()
        #         plt.plot(AppLSLVisu.tabTimestamp[i], AppLSLVisu.tabVal[i])
        #         plt.xlabel("timestamp")
        #         plt.ylabel("value")
        #         plt.title("Graph of the stream " + AppLSLVisu.tabStreams[i].name())
        #
        #         # Trying to remove the previous graph
        #         try:
        #             self.listBoxGraph[i].clear()
        #         except:
        #             pass
        #
        #         # Save the graph in a temporary file
        #         buf = io.BytesIO()
        #         plt.savefig(buf, format='png')
        #         if AppLSLVisu.nbGraphGenerated % 2 == 0 and len(AppLSLVisu.tabTimestamp[1]) > 2:
        #             AppLSLVisu.tabVal[i] = AppLSLVisu.tabVal[i][AppLSLVisu.nbValPlot - 2:]
        #             AppLSLVisu.tabTimestamp[i] = AppLSLVisu.tabTimestamp[i][AppLSLVisu.nbValPlot - 2:]
        #             AppLSLVisu.nbValPlot = 0
        #         fp = tempfile.NamedTemporaryFile()
        #         fp.name = fp.name + AppLSLVisu.tabStreams[i].name()
        #         with open(f"{fp.name}.png", 'wb') as f:
        #             f.write(buf.getvalue())
        #         self.listTempFile.append(fp.name)
        #         plt.close()
        #
        # AppLSLVisu.nbGraphGenerated += 1

    def displayGraph(self, widget):
        """
        Display the graph
        """
        pass
        # # Create the graph
        # self.createGraph()
        #
        # # Create button
        # self.boutonStopChart = toga.Button("Stop generating graph", on_press=self.stopGenerateGraph)
        # self.boxButtonGraph.add(self.boutonStopChart)
        #
        # if AppLSLVisu.streamChoose:
        #     save = self.listTempFile[AppLSLVisu.nbGraphGenerated - 1] + ".png"
        #     self.image = toga.Image(save)
        #     self.imageGraph = toga.ImageView(image=self.image, id=f"view{AppLSLVisu.countId}")
        #     self.listImgGraph[0] = self.imageGraph
        #     self.imageGraph.style.update(width=300, height=300)
        #     self.boxGraph.add(self.imageGraph)
        #     AppLSLVisu.countId += 1
        # else:
        #     # Display the graph
        #     for i in range(len(AppLSLVisu.tabStreams)):
        #         save = self.listTempFile[AppLSLVisu.nbGraphGenerated - 1 + i] + ".png"
        #         self.image = toga.Image(save)
        #         self.imageGraph = toga.ImageView(image=self.image, id=f"view{AppLSLVisu.countId}")
        #         self.listImgGraph[i] = self.imageGraph
        #         self.imageGraph.style.update(width=300, height=300)
        #         self.listBoxGraph[i].add(self.imageGraph)
        #         AppLSLVisu.countId += 1
        #
        # # Remove the button
        # if AppLSLVisu.nbGraphGenerated >= 1:
        #     self.boxButtonGraph.remove(self.buttonGraph)
        #
        # # Start the background task
        # self.add_background_task(self.regenGraph)
        # AppLSLVisu.isGenerateGraph = True

    async def regenGraph(self, widget):
        """
        Regenerate the graph every 3 seconds
        """
        await asyncio.sleep(3)
        pass

        # # Create the graph
        # self.createGraph()
        #
        # if AppLSLVisu.streamChoose:
        #     save = self.listTempFile[AppLSLVisu.nbGraphGenerated - 1] + ".png"
        #     self.image = toga.Image(save)
        #     self.imageGraph = toga.ImageView(image=self.image, id=f"view{AppLSLVisu.countId}")
        #     self.imageGraph.style.update(width=300, height=300)
        #     self.listImgGraph[0] = self.imageGraph
        #     self.boxGraph.add(self.imageGraph)
        #     AppLSLVisu.countId += 1
        # else:
        #     # Display the graph
        #     for i in range(len(AppLSLVisu.tabStreams)):
        #         save = self.listTempFile[AppLSLVisu.nbGraphGenerated - 1 + i] + ".png"
        #         self.image = toga.Image(save)
        #         self.imageGraph = toga.ImageView(image=self.image, id=f"view{AppLSLVisu.countId}")
        #         self.imageGraph.style.update(width=300, height=300)
        #         self.listImgGraph[i] = self.imageGraph
        #         self.listBoxGraph[i].add(self.imageGraph)
        #         AppLSLVisu.countId += 1
        #
        # # Start the background task
        # if AppLSLVisu.isGenerateGraph:
        #     self.add_background_task(self.regenGraph)

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

        # Testing
        box1 = toga.Box()
        box2 = toga.Box()
        box3 = toga.Box()

        resources = os.path.join(AppLSLVisu.app.paths.app, "resources")
        self.img1 = toga.ImageView(image=toga.Image(os.path.join(resources, "flux1.png")))
        self.img2 = toga.ImageView(image=toga.Image(os.path.join(resources, "flux2.png")))
        self.img3 = toga.ImageView(image=toga.Image(os.path.join(resources, "flux3.png")))
        box1.add(self.img1)
        box2.add(self.img2)
        box3.add(self.img3)


        self.bibox = toga.Box(style=Pack(direction=COLUMN))
        self.bibox.add(box1)
        self.bibox.add(box2)
        self.bibox.add(box3)


        boutonTest = toga.Button("aaa",on_press=self.test)

        # Add the button to the box corresponding
        self.boxButtonGetStream.add(self.buttonGetStream)

        # Add the boxes to the main box
        self.mainBox.add(self.boxButtonGetStream)
        self.mainBox.add(self.boxButtonPreference)
        self.mainBox.add(self.boxButtonGraph)
        self.mainBox.add(self.boxButtonRecord)
        self.mainBox.add(boutonTest)

        self.scrolling.content = self.bibox

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
        # try:
        #     self.boxButtonRecord.remove(self.buttonRecordData)
        # except:
        #     pass
        # for i in range(len(AppLSLVisu.tabStreams)):
        #     inlet = stream_inlet(AppLSLVisu.tabStreams[i])
        #     samples, timestamp = inlet.pull_sample()
        #     AppLSLVisu.tabTimestamp[i].append(timestamp)
        #     AppLSLVisu.tabVal[i].append(samples[0])
        # AppLSLVisu.nbValPlot += 1
        # if AppLSLVisu.isRecord:
        #     self.add_background_task(self.recordData)
        # else:
        #     try:
        #         self.boxButtonRecord.remove(self.buttonStopRecord)
        #     except:
        #         pass
        #         pass
        #     self.boxButtonRecord.add(self.buttonRecordData)
        #     AppLSLVisu.isRecord = True

    def getStream(self, widget):
        """
        Get all streams and add all button for start record, generate graph etc.
        """
        # AppLSLVisu.tabStreams = resolve_streams()
        # AppLSLVisu.tabVal = [[0]] * len(AppLSLVisu.tabStreams)
        # AppLSLVisu.tabTimestamp = [[0]] * len(AppLSLVisu.tabStreams)
        # self.listImgGraph = [0] * len(AppLSLVisu.tabStreams)
        self.boxButtonGraph.add(self.buttonGraph)
        self.boxButtonRecord.add(self.buttonRecordData)
        self.boxButtonPreference.add(self.buttonPreference)
        # for i in range(len(AppLSLVisu.tabStreams)):
        #     box = toga.Box(style=Pack(direction=COLUMN), id=f"box{i}")
        #     self.listBoxGraph.append(box)
        #     self.mainBox.add(box)

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
        # listNameOfStream = [stream.name() for stream in AppLSLVisu.tabStreams]
        # listPrint = ""
        # for name in listNameOfStream:
        #     listPrint += "- " + name + "\n"
        # if self.textInput.value in listNameOfStream:
        #     self.main_window.info_dialog("Success", "The stream has been found")
        #     self.boxButtonPreference.remove(self.textInput)
        #     self.boxButtonPreference.remove(widget)
        #     self.boxButtonPreference.remove(self.back)
        #     self.boxButtonPreference.add(self.buttonPreference)
        #     AppLSLVisu.streamChoose = True
        #     self.nameStream = self.textInput.value
        #     self.listBoxGraph = []
        #     self.boxGraph = toga.Box()
        #     self.mainBox.add(self.boxGraph)
        # else:
        #     self.main_window.info_dialog("Error",
        #                                  f"The stream has not been found, please try again\nList stream :\n{listPrint}")

    def backPreference(self, widget):
        self.boxButtonPreference.remove(self.textInput)
        self.boxButtonPreference.remove(self.button)
        self.boxButtonPreference.remove(self.back)
        self.boxButtonPreference.add(self.buttonPreference)

    def test(self,widget):
        print(self.main_window.size)
        size = self.main_window.size
        self.scrolling.content = self.bibox
        self.img1.style.update(width=size[0]*30/100,height=size[0]*30/100)
        self.img2.style.update(width=size[0] * 30 / 100, height=size[0]*30/100)
        self.img3.style.update(width=size[0] * 30 / 100, height=size[0]*30/100)
        print("widht="+str(size[0]*30/100))
        print("height="+str(size[1]*30/100))


def getStream(listStream: list, nameStream: str):
    """
    :param listStream: list of LSL Streams
    :param nameStream: String of name in list
    :return : The place of the stream with the name in parameters
    """
    pass
    # listName = [stream.name() for stream in listStream]
    # return listName.index(nameStream)


def main():
    return AppLSLVisu()
