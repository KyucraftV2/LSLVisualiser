"""
My first application
"""
import asyncio

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
#import toga_chart
import numpy as np
#import pyxdf


class HelloWorld(toga.App):
    MU = 100  # mean of distribution
    SIGMA = 15  # standard deviation of distribution

    def set_data(self):
        # Generate some example data
        #self.x = self.MU + self.SIGMA * np.random.randn(437)
        pass

    def draw_chart(self, chart, figure, *args, **kwargs):
        #streams, header = pyxdf.load_xdf(r'C:\Users\killian\Desktop\appLSLVisu\appvisulsl\src\appvisulsl\resources\data.xdf')
        #data = streams[0]["time_series"]
        # y = []
        # for test in streams[1]["time_series"]:
        #     y.append(test)
        #
        # # Add a subplot that is a histogram of the data,
        # # using the normal matplotlib API
        # ax = figure.add_subplot(1,1,1)
        # ax.plot(streams[1]["time_stamps"],y,'--')
        # ax.set_xlabel('Value')
        # ax.set_ylabel('Probability density')
        # ax.set_title(r'Diagramme Test')
        #
        # figure.tight_layout()
        pass

    def nextChart(self,figure):
        pass
        # streams, header = pyxdf.load_xdf(
        #     r'C:\Users\killian\Desktop\appLSLVisu\appvisulsl\src\appvisulsl\resources\oldData.xdf')
        # data = streams[0]["time_series"]
        # y = []
        # for test in streams[1]["time_series"]:
        #     y.append(test)
        #
        # # Add a subplot that is a histogram of the data,
        # # using the normal matplotlib API
        # ax = figure.add_subplot(1, 1, 1)
        # ax.plot(streams[1]["time_stamps"], y, '--')
        # ax.set_xlabel('Value')
        # ax.set_ylabel('Probability density')
        # ax.set_title(r'Diagramme Test')
        #
        # figure.tight_layout()


    def startup(self):

        # np.random.seed(19680801)
        # self.set_data()
        #
        # # Set up main window
        # self.main_window = toga.MainWindow(title=self.name)
        #
        # self.chart = toga_chart.Chart(style=Pack(flex=1), on_draw=self.draw_chart)
        #
        # self.main_window.content = toga.Box(
        #     children=[
        #         self.chart,
        #         toga.Button("Recreate data",on_press=self.changeTitle)
        #     ],
        #     style=Pack(direction=COLUMN)
        # )

        self.text_appearance = True

        # Add components to the main box
        self.main_box = toga.Box(style=Pack(direction=COLUMN))
        self.label = toga.Label("this text is flashing")
        self.main_box.add(self.label)

        self.liste = toga.Label(np.array([1,2,3,4,5,6,7,89]))
        self.main_box.add(self.liste)

        # Show main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()
        self.add_background_task(self.flash)
        self.add_background_task(self.changeTitle)
        self.add_background_task(self.changeTitleAlso)

    def flash(self, widget):
        yield 0.5
        if self.text_appearance:
            self.main_box.remove(self.label)
            self.text_appearance = False
        else:
            self.main_box.add(self.label)
            self.text_appearance = True
        self.add_background_task(self.flash)

    def changeTitle(self,widget):
        yield 1
        self.main_window.title = "Il est tard"

    async def changeTitleAlso(self,widget):
        await asyncio.sleep(3)
        self.main_window.title = "Il est vraiment tard"



def main():
    return HelloWorld()
