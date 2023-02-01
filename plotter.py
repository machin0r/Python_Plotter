import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import tkinter
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk

print(matplotlib.get_backend()) # Required to not use agg, so plot is shown

line5 = (0, (3, 1, 1, 1, 1, 1))
lineStyleList = ["-", "--", "-.", ":", line5]


class PlotObject:
    """ Object template that will contain each data set to plot"""

    def __init__(self, xValues, yValues, label):
        self.xValues = xValues
        self.yValues = yValues
        self.label = label


class Plotter(ttk.Frame):
    """The Plotter gui and functions."""

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_gui()
        self.plotDict = {}
        self.csvFile = ""

    def on_quit(self):
        """Exits program."""
        quit()

    def opencsvFile(self):
        """Opens the data file via user selection"""
        self.csvFile = filedialog.askopenfilename()
        print((self.csvFile))
        textOutputVar = "File loaded \n"
        self.outputtext['text'] = textOutputVar

        
    def dataRead(self):
        """Read in the data from the file to a pandas dataframe"""
        """Iterate through the data and create a PlotObject for each dataset"""
        """These PlotObjects are then stored in a dictionary to be called later"""
        self.plotDict = {}
        inputDataFrame = pd.read_csv(self.csvFile)  # Read in data from a csv file
        headings = inputDataFrame.columns.values.tolist()  # Gets all header names

        headings = headings[:-1]
        xLimLower = inputDataFrame.at[1, 'X1']
        yLimLower = inputDataFrame.at[1, 'Y1']
        xLimUpper = inputDataFrame.at[1, 'X1']
        yLimUpper = inputDataFrame.at[1, 'Y1']

        for a in range(1, ((len(headings) // 2) + 1)):
            ('X' + str(a + 1))
            self.plotDict[a] = PlotObject(inputDataFrame[('X' + str(a))].values, inputDataFrame[('Y' + str(a))].values,
                                          inputDataFrame.at[a - 1, 'Labels'])
            xLimLowerTemp = np.amin(inputDataFrame[('X' + str(a))].values) * 0.9
            xLimUpperTemp = np.amax(inputDataFrame[('X' + str(a))].values) * 1.1
            yLimLowerTemp = np.amin(inputDataFrame[('Y' + str(a))].values) * 0.9
            yLimUpperTemp = np.amax(inputDataFrame[('Y' + str(a))].values) * 1.1
            # Determines if the current X Y value is a higher/lower than the plot limits
            # It replaces the current limit if so
            if xLimLowerTemp < xLimLower:
                xLimLower = xLimLowerTemp
            if xLimUpperTemp > xLimUpper:
                xLimUpper = xLimUpperTemp
            if yLimLowerTemp < yLimLower:
                yLimLower = yLimLowerTemp
            if yLimUpperTemp > yLimUpper:
                yLimUpper = yLimUpperTemp
        return xLimLower, yLimLower, xLimUpper, yLimUpper

    def plotGraph(self):
        """Main plotter function where each PlotObject is plotted to a graph"""

        xAxisTitle = self.xAxisTitle.get()
        yAxisTitle = self.yAxisTitle.get()
        graphTitle = self.graphTitle.get()
        scatter = self.scatterVar.get()
        regression = self.regressionVar.get()
        regressionPower = self.regressionPower.get()

        xLimLower, yLimLower, xLimUpper, yLimUpper = self.dataRead()
        print("Created data frame from file...")
        textOutputVar = "Created data frame from file... \n"
        self.outputtext['text'] = textOutputVar
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        a = 0

        for key in self.plotDict:
            if scatter == 1:
                plt.plot(self.plotDict[key].xValues, self.plotDict[key].yValues, '.', label=self.plotDict[key].label)
            if scatter == 0:
                plt.plot(self.plotDict[key].xValues, self.plotDict[key].yValues, '.', label=self.plotDict[key].label,
                         linestyle=lineStyleList[a])
            if regression == 1:
                fitting = np.polyfit(self.plotDict[key].xValues, self.plotDict[key].yValues, int(regressionPower), full=True)
                coef = fitting [0]
                SSE = fitting[1][0]  # Sum of Square Errors
                SSEdiff = self.plotDict[key].yValues - self.plotDict[key].yValues.mean()
                square_diff = SSEdiff ** 2
                SST = square_diff.sum()  # Sum of Square Total
                R2 = 1 - SSE/SST 
                poly1d_fn = np.poly1d(coef)
                textOutputVar += (str(self.plotDict[key].label) + " polyfit is: " + str(poly1d_fn) + " with an R2 of: " 
                        + str(R2) + "\n")
                self.outputtext['text'] = textOutputVar
                plt.plot(self.plotDict[key].xValues, poly1d_fn(self.plotDict[key].xValues),
                         label=self.plotDict[key].label)
            a += 1

        textOutputVar += "Data Plotted \n"
        self.outputtext['text'] = textOutputVar

        plt.xlabel(xAxisTitle, fontsize=14)
        plt.ylabel(yAxisTitle, fontsize=14)
        plt.xlim([xLimLower, xLimUpper])
        plt.ylim([yLimLower, yLimUpper])
        ax.grid()
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.tick_params(which='major', color='black')
        ax.tick_params(which='minor', color='black')
        plt.title(graphTitle)
        legend = ax.legend(loc='upper left', shadow=True)

        plt.show()

        self.answer_label['text'] = 'Complete'

    # Builds the GUI
    def init_gui(self):
        """Builds GUI."""
        self.root.title('Plotter')
        self.root.option_add('*tearOff', 'FALSE')

        self.grid(column=0, row=0, sticky='nsew')

        # Creates menubar
        self.menubar = tkinter.Menu(self.root)

        # Adds an exit command to the file menu bar option
        self.menu_file = tkinter.Menu(self.menubar)
        self.menu_file.add_command(label='Exit', command=self.on_quit)
        self.menu_edit = tkinter.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label='File')
        self.root.config(menu=self.menubar)

        # Button to control the opening of the files
        self.file1_button = ttk.Button(self, text='Open csv File',
                                       command=self.opencsvFile)
        self.file1_button.grid(column=0, row=4, columnspan=4)

        # Once files chosen, displays file path
        self.csvFileSelectedFrame = ttk.LabelFrame(self, text='Input File',
                                                     height=100)
        self.csvFileSelectedFrame.grid(column=0, row=3, columnspan=4, sticky='nesw')

        self.csvFileSelected = ttk.Label(self.csvFileSelectedFrame, text='')
        self.csvFileSelected.grid(column=0, row=0)

        self.graphTitle = ttk.Entry(self, width=15)
        self.graphTitle.grid(column=2, row=5)
        ttk.Label(self, text='Graph Title').grid(column=1, row=5,
                                                 sticky='w')

        self.xAxisTitle = ttk.Entry(self, width=15)
        self.xAxisTitle.grid(column=2, row=6)
        ttk.Label(self, text='X Axis').grid(column=1, row=6,
                                            sticky='w')

        self.yAxisTitle = ttk.Entry(self, width=15)
        self.yAxisTitle.grid(column=2, row=7)
        ttk.Label(self, text='Y Axis').grid(column=1, row=7,
                                            sticky='w')

        self.scatterVar = tk.IntVar()
        ttk.Checkbutton(self, text='Scatter (Default is line)', variable=self.scatterVar, onvalue=1,
                        offvalue=0).grid(column=1, row=8, sticky='w')

        self.regressionVar = tk.IntVar()
        ttk.Checkbutton(self, text='Regression Fit', variable=self.regressionVar, onvalue=1,
                        offvalue=0).grid(column=1, row=9, sticky='w')

        self.regressionPower = ttk.Entry(self, width=15)
        self.regressionPower.grid(column=3, row=9)
        ttk.Label(self, text='Regression Power').grid(column=2, row=9,
                                                      sticky='w')

        # Button to start collation process
        self.calc_button = ttk.Button(self, text='Plot',
                                      command=self.plotGraph)
        self.calc_button.grid(column=0, row=13, columnspan=4)

        # Has a space to tell the user if the process is completed
        self.answer_frame = ttk.LabelFrame(self, text='Finished?',
                                           height=100)
        self.answer_frame.grid(column=0, row=14, columnspan=4, sticky='nesw')

        self.answer_label = ttk.Label(self.answer_frame, text='')
        self.answer_label.grid(column=0, row=0)

        self.outputtextFrame = ttk.LabelFrame(self, text='Output',
                                              height=100)
        self.outputtextFrame.grid(column=0, row=15, columnspan=4, sticky='nesw')

        self.outputtext = ttk.Label(self.outputtextFrame, text='')
        self.outputtext.grid(column=0, row=16)

        # Labels that remain constant throughout execution.
        ttk.Label(self, text='Choose the input File - order columns as (x1,y1,x2,y2...xn,yn, Labels)').grid(
            column=0, row=0, columnspan=4)

        ttk.Separator(self, orient='horizontal').grid(column=0, row=1, columnspan=4, sticky='ew')

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)


if __name__ == '__main__':
    root = tkinter.Tk()
    Plotter(root)
    root.mainloop()
