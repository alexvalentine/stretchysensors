

import matplotlib.pylab as plt
import numpy as np
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import pandas as pd
import argument_parser as argpars
import scipy.stats as ss

import sys

# pythonana plot.py -inputfile 1_importing_alpha.csv -xpos 0 -ypos 1,2:3
# -legend -xaxes 1,2 -show
# by the optional arguments, the function can also be used from data, which is generated in python
# xdata and ydata options still have to be implemented.
# Preconditions:
# - data: list object containing the data as arrays to plot
# - xdata: number that specifies which line is the xdata, default is 0
# - ydata: integer that specifies which lines are the ydata to plot, default is 1 to len(data)
#
# Example usage, together with csvImporter class, which returns a dict object.
# plotobject = {
        # 		"data":list(imported_data.data.values()),
        # 		"xdata":2,
        # 		"ydata":[0,1],
        # 		"savefig":"test",
        # 		"xlabel":"test",
        # 		"ylabel":"test",
        # 		"title":"test",
        # 		"linestyle":"*"
        # }
        #
# plot.my_plot(plotobject)
#
# if use for formatting plots only:
#     plotobject = {
    #     "figure": 2,
    #     "savefig": "Syringe_10ml_initial1",
    #     "xaxes": "0.005, 100",
    #     "xlabel": r"strain [%]",
    #     "ylabel": r"G'/G'' [Pa]",
    #     "loglog": "test"
    # }

# example of errorbarplot:
# plotobject = {
    #     "figure": 3,
    #     "specialplot": "errorbarplot",
    #     "data": [x,y1,y2,y3],
    #     "savefig": "weight_change_ink",
    #     "color": "blue",
    #     "yaxes": "9.8, 14",
    #     "xlabel": "time [h]",
    #     "ylabel": "total weight [g]"
    # }
    # plot.my_plot(plotobject)
# calculates the errorbarplot, with confidence intervals for y1,y2,y3.


class my_plot(object):

        # optional argument data
    def __init__(self, arg, main=1):

        # parse all arguments into a telefon book:

        argparser = argpars.argument_parser()

        self.tel = argparser.read(arg)
        self.plt = plt

        if main == 1:
            self.main()

    def main(self):

        self.figure()

        if "data" in self.tel.keys():
            self.data()
            # check if the data is entered as a nested list, then rearrange the
            # data, that it has only [[],[],[]] twok list levels at most.

            def Resolve_nested_lists():

                for x in xrange(0, len(self.data)):
                    try:
                        if type(self.data[x][0]) == list:

                            nested_list = self.data[x]
                            del self.data[x]
                            for j in xrange(0, len(nested_list)):
                                self.data.insert(x + j, nested_list[j])
                            Resolve_nested_lists()

                    except Exception, e:
                        pass

            Resolve_nested_lists()

# default for xdata is the first line
        if "xdata" not in self.tel.keys():
            self.xdata = 0
        else:
            self.xdata = self.tel["xdata"]
# default for ydata are all the other lines
        if "ydata" not in self.tel.keys():
            if "data" in self.tel.keys():
                self.ydata = range(1, len(self.data))

        else:
            self.ydata = self.tel["ydata"]

        # always draw the grid by default.
        # if "grid" not in self.tel.keys():
        #     plt.grid()

        self.fontsize()
        self.xlabel()
        self.ylabel()
        self.title()
        self.xaxes()
        self.yaxes()
        self.loglog()
        self.xlog()
        self.ylog()
        self.legendentries()
        self.linestyle()
        self.marker()

        if "specialplot" in self.tel.keys():

            if self.tel["specialplot"] == "boxplot":
                plt.boxplot(self.data)
                if "xticklabels" in self.tel.keys():
                    plt.xticks(
                        range(1, len(self.tel["xticklabels"]) + 1), self.tel["xticklabels"])

            if self.tel["specialplot"] == "errorbarplot":

                def mean_confidence_interval(data, confidence=0.95):
                    n = len(data)
                    m, se = np.mean(data), ss.sem(data)
                    h = se * \
                        ss.t._ppf(
                            (1 + confidence) / 2., n - 1)
                    return m, h

                # What if y data is a list of lists....

                if "legend" in self.tel.keys():

                    for i in range(0, len(self.ydata)):

                        mean, yerr = mean_confidence_interval(
                            self.data[self.ydata[i]])

                        plt.errorbar(self.data[self.xdata][
                                     i], mean, yerr=yerr, label=self.legendentries, linewidth=2, marker='s', ls='-', color=self.tel["color"])

                    plt.legend(
                        loc=self.tel["legend"], prop={'size': self.fontsize - 8})
                else:
                    for i in range(0, len(self.ydata)):

                        mean, yerr = mean_confidence_interval(
                            self.data[self.ydata[i]])

                        plt.errorbar(self.data[self.xdata][
                                     i], mean, yerr=yerr, linewidth=2, marker='s', ls='-', color=self.tel["color"])
        else:
            if"data" in self.tel.keys():
                self.plot()

        if "savefig" in self.tel.keys():
            self.savefig()

    def data(self):
        self.data = self.tel["data"]

    def figure(self):
        if "figure" in self.tel.keys():
            if self.tel["figure"] is not "not set":
                plt.figure(self.tel["figure"])
            else:
                plt.figure()

    def fontsize(self):

        if "fontsize" in self.tel.keys():
            if self.tel["fontsize"] is not "not set":
                self.fontsize = self.tel["fontsize"]
        else:
            self.fontsize = 24
        plt.yticks(fontsize=self.fontsize - 8)
        plt.xticks(fontsize=self.fontsize - 8)

    def xlabel(self):

        if "xlabel" in self.tel.keys():
            plt.xlabel(self.tel["xlabel"], fontsize=self.fontsize - 4)

    def ylabel(self):

        if "ylabel" in self.tel.keys():
            plt.ylabel(self.tel["ylabel"], fontsize=self.fontsize - 4)

    def title(self):
        if "title" in self.tel.keys():
            plt.title(self.tel["title"], fontsize=self.fontsize)

    def xaxes(self):
        if "xaxes" in self.tel.keys():
            plt.xlim(map(float, self.tel["xaxes"].split(",")))

    def yaxes(self):
        if "yaxes" in self.tel.keys():
            plt.ylim(map(float, self.tel["yaxes"].split(",")))

    def loglog(self):
        if "loglog" in self.tel.keys():
            plt.xscale('log')
            plt.yscale('log')

    def xlog(self):
        if "xlog" in self.tel.keys():
            plt.xscale('log')

    def ylog(self):
        if "ylog" in self.tel.keys():
            plt.yscale('log')

    def legendentries(self):
        if "legendentries" in self.tel.keys():
            self.legendentries = self.tel["legendentries"].split(",")

    def linestyle(self):
        if "linestyle" in self.tel.keys():
            self.linestyle = self.tel["linestyle"]
        else:
            self.linestyle = "-"

    def marker(self):
        if "marker" in self.tel.keys():
            self.marker = self.tel["marker"]
        else:
            self.marker = "None"

    def plot(self):

        # plots either with or without legend
        if "legend" in self.tel.keys():

            plt.legend(
                loc=self.tel["legend"], prop={'size': self.fontsize - 8})

            for i in range(0, len(self.ydata)):

                plt.plot(self.data[self.xdata], self.data[self.ydata[i]], label=self.legendentries[
                         i], linewidth=2, marker=self.marker, ls=self.linestyle)
            plt.legend(
                loc=self.tel["legend"], prop={'size': self.fontsize - 8})
        else:
            for i in range(0, len(self.ydata)):
                plt.plot(self.data[self.xdata], self.data[self.ydata[i]],
                         linewidth=2, marker=self.marker, ls=self.linestyle)

    def savefig(self):
        plt.savefig(self.tel["savefig"] + ".pdf", format='pdf')

    def show(self):
        if "show" in self.tel.keys():
            plt.show()


if __name__ == "__main__":
    print("main")
