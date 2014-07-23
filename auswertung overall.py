import matplotlib.pylab as plt
import numpy as np
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


# from this file, generate a Template for later work!!!

if __name__ == "__main__":

    tau = [[], [], [], []]
    x = [0, 50, 100, 150]

    # First import all the 32 files.

    DoAnalysis("20140417-01_ne_oc_", "0", tau[0])
    DoAnalysis("20140417-01_e50_oc_", "50", tau[1])
    DoAnalysis("20140417-01_e100_oc_", "100", tau[2])
    DoAnalysis("20140417-01_e150_oc_", "150", tau[3])

    plt.close("all")

    plotobject = {

        "figure": 1,
        "specialplot": "errorbarplot",
        "data": [x, tau],
        "savefig": "Sensor1_confidence_intervals",
        "xticklabels": ["0", "50", "100", "150"],
        "xlabel": "strain [%]",
        "color": "blue",
        "xaxes": "-10,160",
        "ylabel": "Time Constant [ms]",
        "title": "Sensor 1"

    }

    test_set = {
        "file": "data_for_boxplot.csv",
        "header": "F",
        "data": tau
    }

    csvExp.csvExport(test_set)

    plot.my_plot(plotobject)

    # You need a template that just has a
    # make a statistics and draw the distribution.
