

import matplotlib.pylab as plt
import numpy as np
from matplotlib import rcParams
# rcParams.update({'figure.autolayout': True})
import pandas as pd
import argument_parser as argpars
import scipy.stats as ss

import sys

# if use for formatting anykind of plots:
#     plotobject = {
    #     "figure": 2,
    #     "axes": ax,
    #     "savefig": "Syringe_10ml_initial1",
    #     "xlabel": r"strain [%]",
    #     "ylabel": r"G'/G'' [Pa]",
    #     "loglog": "test"
    # }
    # plot_form.my_plot(plotobject)


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
        self.axes()
        self.fontsize()
        self.legend()
        self.xlabel()
        self.ylabel()
        self.yaxiscolor()
        self.title()
        self.loglog()
        self.xlog()
        self.ylog()
        self.savefig()

        # if "grid" not in self.tel.keys():
        #     plt.grid()

    def figure(self):
        if "figure" in self.tel.keys():
            if self.tel["figure"] is not "not set":

                if type(self.tel["figure"]) is int:
                    self.fig = self.plt.figure(self.tel["figure"])

                    if self.fig.get_axes() == []:
                        self.plt.plot()

                else:
                    self.fig = self.tel["figure"]

            else:
                plt.figure()

    def axes(self):

        if "axes" in self.tel.keys():
            self.axes = self.tel["axes"]
        else:
            self.axes = self.fig.get_axes()[0]

    def fontsize(self):

        if "fontsize" in self.tel.keys():
            if self.tel["fontsize"] is not "not set":
                self.fontsize = self.tel["fontsize"]
        else:
            self.fontsize = 24
        # for tick in self.axes.xaxis.get_major_ticks():
        #     tick.label.set_fontsize(self.fontsize - 8)

        self.axes.tick_params(
            axis='both', which='major', labelsize=self.fontsize - 10)
        # for tick in self.axes.yaxis.get_major_ticks():
        #     tick.label.set_fontsize(self.fontsize - 20)

    def xlabel(self):

        if "xlabel" in self.tel.keys():
            self.axes.set_xlabel(
                self.tel["xlabel"], fontsize=self.fontsize - 4)

    def ylabel(self):

        if "ylabel" in self.tel.keys():
            self.axes.set_ylabel(
                self.tel["ylabel"], fontsize=self.fontsize - 4)

    def title(self):
        if "title" in self.tel.keys():
            self.axes.set_title(self.tel["title"], fontsize=self.fontsize)

    def loglog(self):
        if "loglog" in self.tel.keys():
            self.axes.set_xscale('log')
            self.axes.set_yscale('log')

    def xlog(self):
        if "xlog" in self.tel.keys():
            self.axes.set_xscale('log')

    def ylog(self):
        if "ylog" in self.tel.keys():
            self.axes.set_yscale('log')

    def yaxiscolor(self):

        if "yaxiscolor" in self.tel.keys():
            self.axes.yaxis.label.set_color(self.tel["yaxiscolor"])

    def legend(self):

        if "legend" in self.tel.keys():
            leg = self.axes.legend(
                loc=self.tel["legend"], prop={'size': self.fontsize - 8})

            # llines = leg.get_lines()  # all the lines

            # plt.setp(llines, markerfacecolor='r',
            #          markeredgecolor='r', color='k')
            #
            leg.draw_frame(False)

    def savefig(self):
        if "savefig" in self.tel.keys():
            plt.savefig(self.tel["savefig"] + ".pdf", format='pdf')


if __name__ == "__main__":
    print("main")
