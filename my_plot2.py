

import matplotlib.pylab as plt
import numpy as np
from matplotlib import rcParams
# rcParams.update({'figure.autolayout': True})
import pandas as pd
import argument_parser as argpars
import scipy.stats as ss

import sys


# This library is mend to be used together with the plot formatting library


# by the optional arguments, the function can also be used from data, which is generated in python
# xdata and ydata options still have to be implemented.
# Preconditions:
# - data: list object containing the data as arrays to plot
# - xdata: number that specifies which line is the xdata, default is 0
# - ydata: integer that specifies which lines are the ydata to plot, default is 1 to len(data)
#
# Example usage, together with csvImporter class, which returns a dict object.
# plotobject = {
#     "figure": i,
#     "data": [test.data["Time"], test.data["Signal"] / 1024],
#     "legendentries": ["Strain 50 %"]
# }

# plot.my_plot2(plotobject)

# plotobject = {
#     "figure": i,
#     "savefig": r"plots/Sensor" + str(Sensornumber[i]) + "RawSignal",
#     "xlabel": r" Time [$\mu$s]",
#     "ylabel": r"$V_{Rm}$",
#     "legend": "True"
# }

# plot_form.my_plot(plotobject)


class my_plot2(object):

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
        self.axes()

        if "data" in self.tel.keys():
            self.data()
            # check if the data is entered as a nested list, then rearrange the
            # data, that it has only [[],[],[]] twok list levels at most.

            def Resolve_nested_lists():

                for x in xrange(0, len(self.data)):
                    try:
                        print type(self.data[x][0])
                        if type(self.data[x][0]) == list or type(self.data[x][0]) == np.ndarray:
                            print self.data
                            nested_list = self.data[x]
                            del self.data[x]
                            for j in xrange(0, len(nested_list)):
                                self.data.insert(x + j, nested_list[j])
                            Resolve_nested_lists()

                    except Exception, e:
                        print e

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

        self.xaxes()
        self.yaxes()
        self.legendentries()
        self.linestyle()
        self.linewidth()
        self.marker()
        self.color()

        if "specialplot" in self.tel.keys():

            if self.tel["specialplot"] == "boxplot":
                self.plt.boxplot(self.data)
                if "xticklabels" in self.tel.keys():
                    self.plt.xticks(
                        range(1, len(self.tel["xticklabels"]) + 1), self.tel["xticklabels"])

            # the legendentry of an errorbarplot can only be one
            if self.tel["specialplot"] == "errorbarlineplot":

                def mean_confidence_interval(data, confidence=0.95):
                    n = len(data)
                    m, se = np.mean(data), ss.sem(data)
                    h = se * \
                        ss.t._ppf(
                            (1 + confidence) / 2., n - 1)
                    return m, h
# The function should have the ability to easily plot quantiles
#

                def percentile(data, lower_percentile, upper_percentile):

                    m = np.mean(data)
                    h1 = m - np.percentile(data, lower_percentile)
                    h2 = np.percentile(data, upper_percentile) - m

                    return m, h1, h2

                # What if y data is a list of lists....

                mean = []
                yerrhilf1 = []
                yerrhilf2 = []
                yerr = []

                for i in range(0, len(self.ydata)):

                    if "percentiles" in self.tel.keys():

                        meanhilf, yerrhil1, yerrhil2 = percentile(
                            self.data[self.ydata[i]], self.tel["percentiles"][0], self.tel["percentiles"][1])
                        mean.append(meanhilf)
                        yerrhilf1.append(yerrhil1)
                        yerrhilf2.append(yerrhil2)
                        yerr = [yerrhilf1, yerrhilf2]

                    if "confidence_intervals" in self.tel.keys():

                        meanhilf, yerrhilf = mean_confidence_interval(
                            self.data[self.ydata[i]], float(self.tel["confidence_intervals"]))
                        mean.append(meanhilf)
                        yerr.append(yerrhilf)

                if "legendentries" in self.tel.keys():

                    self.plt.errorbar(
                        self.data[
                            self.xdata], mean, yerr=yerr, label=self.legendentries,
                        linewidth=2, marker=self.marker[0], ls=self.linestyle[0])

                else:

                    self.plt.errorbar(
                        self.data[self.xdata], mean, yerr=yerr, linewidth=2, marker=self.marker[0], ls=self.linestyle[0])

            if self.tel["specialplot"] == "continous_error_area_plot":
                # preconditions:
                # - ydata must be a list of numpy arrays as for the errorbarplot

                maxs = list(self.data[self.ydata[0]])
                mins = list(self.data[self.ydata[0]])
                hilf = list(self.data[self.ydata[0]])

                for i in range(1, len(self.ydata)):

                    if "min_max" in self.tel.keys():

                        for j in xrange(0, len(self.data[self.ydata[i]])):

                            hilf[j] = hilf[j] + \
                                self.data[self.ydata[i]][j]

                            if maxs[j] < self.data[self.ydata[i]][j]:
                                maxs[j] = self.data[self.ydata[i]][j]

                            if mins[j] > self.data[self.ydata[i]][j]:
                                mins[j] = self.data[self.ydata[i]][j]

                means = []
                means = list(np.asarray(hilf) / len(self.ydata))

                self.ydata = [1]
                self.data[self.ydata[0]] = means

                self.plot()

                self.axes.fill_between(
                    self.data[self.xdata], mins, maxs, facecolor=self.line[0].get_color(), alpha=0.3)

        else:

            if"data" in self.tel.keys():
                self.plot()

    def plot(self):

        # plots either with or without legend

        self.line = []

        if "legendentries" in self.tel.keys():

            for i in range(0, len(self.ydata)):

                baseline, = self.axes.plot(self.data[self.xdata], self.data[self.ydata[i]], label=self.legendentries[
                    i], linewidth=self.linewidth[i], marker=self.marker[i], ls=self.linestyle[i])

                self.line.append(baseline)

        else:
            for i in range(0, len(self.ydata)):

                baseline, = self.axes.plot(
                    self.data[self.xdata], self.data[self.ydata[i]],
                    linewidth=self.linewidth[i], marker=self.marker[i], ls=self.linestyle[i])

                self.line.append(baseline)

    def data(self):

        self.data = self.tel["data"]

    def color(self):

        if "color" in self.tel.keys():

            self.axes.set_color_cycle(self.tel["color"])

    def figure(self):
        if "figure" in self.tel.keys():
            if self.tel["figure"] is not "not set":

                if type(self.tel["figure"]) is int:
                    self.fig = plt.figure(self.tel["figure"])

                    if self.fig.get_axes() == []:
                        self.plt.plot()

                else:
                    self.fig = self.tel["figure"]

                    if self.fig.get_axes() == []:
                        self.plt.plot()
            else:
                self.plt.figure()

    def axes(self):

        if "axes" in self.tel.keys():
            self.axes = self.tel["axes"]
        else:
            self.axes = self.fig.get_axes()[0]

    def xaxes(self):
        if "xaxes" in self.tel.keys():
            self.axes.set_xlim(map(float, self.tel["xaxes"]))

    def yaxes(self):
        if "yaxes" in self.tel.keys():
            self.axes.set_ylim(map(float, self.tel["yaxes"]))

    def legendentries(self):
        if "legendentries" in self.tel.keys():
            self.legendentries = self.tel["legendentries"]

    def linestyle(self):
    # must be of type list
        if "linestyle" in self.tel.keys():

            if len(self.tel["linestyle"]) == 1:

                self.linestyle = self.tel["linestyle"] * len(self.ydata)

            self.linestyle = self.tel["linestyle"]

        else:

            self.linestyle = ["-"] * len(self.ydata)

    def linewidth(self):
    # must be of type list
        if "linewidth" in self.tel.keys():

            if len(self.tel["linewidth"]) == 1:

                self.linewidth = self.tel["linewidth"] * len(self.ydata)

            self.linewidth = self.tel["linewidth"]

        else:

            self.linewidth = [2] * len(self.ydata)

    def marker(self):
        if "marker" in self.tel.keys():

            if len(self.tel["marker"]) == 1:

                self.marker = self.tel["marker"] * len(self.ydata)

            self.marker = self.tel["marker"]
        else:
            self.marker = ["s"] * len(self.ydata)

    def savefig(self):
        self.plt.savefig(self.tel["savefig"] + ".pdf", format='pdf')

    def show(self):
        if "show" in self.tel.keys():
            self.plt.show()


if __name__ == "__main__":
    print("main")
