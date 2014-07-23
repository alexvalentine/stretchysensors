import matplotlib.pylab as plt
import numpy as np
import pandas as pd
from scipy.signal import butter, lfilter, filtfilt, firwin
from scipy.optimize import curve_fit
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import operator
from scipy import stats

import sys
sys.path.append("/Volumes/Daten/ds_Admin_Andreas/Studium/Vorlagen/Phyton")
sys.path.append(
    "/Volumes/Daten/ds_Admin_Andreas/Studium/Vorlagen/Phyton/Masterthesis_Readout_files")


import csvImport as csvImp
import csvExport as csvExp
import my_plot as plot
import Signal_processing as sig
from Time_constant_calculation_Sensor import DoAnalysis


# this script is used in order to draw a the model prediction over the
# data obtained from the sensors.

def CalculateFit(strain, init, init_strain):

    C = float(init) / float((float(init_strain) + 1) ** 3)
    tau = []
    print C
    for item in strain:
        tau.append(C * (1 + float(item)) ** 3)

    return tau
    # first calculate the constant in order to fit it to the data

if __name__ == "__main__":

# first read the data file
#

    filename = "data_for_boxplot.csv"

    test_set = {
        "file":
        filename,
        "header":
        "F",
        # if header is not true then the names of the variables can
        # bespecified
        "names":
        ["a", "b", "c", "d"],
        "HasUnits":
        "F",
        "Units":
        ["[m]", "[s]", "[kg/s]"],
        "LinesToSkip":
        [0],
        "PrintContent":
        "T"
    }

    imported = csvImp.csvImport(test_set)
    # csv import does not work

    data = pd.read_csv("data_for_boxplot.csv", names=["a", "b", "c", "d"])

    x = [0, 50, 100, 150]

    plt.show()

    a = range(150)

    test = map(lambda x: x / float(100), a)

    print test
    y = [np.mean(data["a"]), np.mean(data["b"]),
         np.mean(data["c"]), np.mean(data["d"])]
    print y
    # plt.figure(1)
    # plt.plot(a, CalculateFit(test, np.mean(data["a"]), 0))
    # p3 = np.polyfit(x, y, 3)
    # c3 = np.polyval(p3, a)
    # plt.plot(a, c3)
    # p2 = np.polyfit(x, y, 2)
    # c2 = np.polyval(p2, a)
    # plt.plot(a, c2)
    # p1 = np.polyfit(x, y, 1)
    # c1 = np.polyval(p1, a)
    # plt.plot(a, c1)

    y = CalculateFit(test, np.mean(data["a"]), 0)

    plotobject = {
        "figure":
        1,
        "data":
        [a, y],
        "savefig":
        "comparison_with_Sensor_model",
        "xlabel":
        "strain [%]",
        "ylabel":
        "Time constant [ms]",
        "title":
        "Comparison with Sensor model",
        "color":
        "red"
    }

    plot.my_plot(plotobject)

    plotobject = {
        "figure":
        1,
        "data":
        [x, data["a"], data["b"], data["c"], data["d"]],
        "specialplot":
        "errorbarplot",
        "savefig":
        "Sensor 1",
        "xlabel":
        "strain [%]",
        "ylabel":
        "Time constant [ms]",
        "title":
        "Sensor 1",
        "color":
        "red"
    }

    plot.my_plot(plotobject)
