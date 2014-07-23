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


import csvImport as csvImp
import csvExport as csvExp
import my_plot as plot
import Signal_processing as sig


# from this file, generate a Template for later work!!!
def func(x, a, b):
    return a * x + b


def CalculateEnergyOfSignal(signal):

    for x in xrange(10, len(signal)):
        signal[x] = signal[x] ** 2

    return signal


def DoAnalysis(file, Dehnung, tau):

    R_square = []

    for k in xrange(1, 2):
        print k

        if k < 10:
            filename = file + "0" + str(k) + ".csv"
        else:
            filename = file + str(k) + ".csv"

        test_set = {
            "file": filename,
            "header": "T",
            # if header is not true then the names of the variables can
            # bespecified
            "names": ["x", "y", "z"],
            "HasUnits": "T",
            "Units": ["[m]", "[s]", "[kg/s]"],
            "LinesToSkip": [2],
            "PrintContent": "F"
        }
        # try to import the file, if not then just continue.
        try:
            imported_data = csvImp.csvImport(test_set)
        except Exception, e:
            continue

        # calculate the width of the peak finder as the difference of the second
        # and third entry in the zerocrossing vector.
        # filter the signal
        N = 10
        Fc = 1000
        Fs = 1600
        # provide them to firwin
        h = firwin(numtaps=N, cutoff=40, nyq=Fs / 2)

        # 'x' is the time-series data you are filtering
        filtered_signal = lfilter(h, 1.0, imported_data.data["Kanal A"])
        input_signal = imported_data.data["Kanal B"]

        plt.close("all")
        plotobject = {
            "figure": 1,
            "data": [imported_data.data["Zeit"], imported_data.data["Kanal A"], filtered_signal],
            "savefig": "filtered_unfiltered_signal" + "D" + Dehnung + "_No" + str(k),
            "legend": "T",
            "legendentries": "before filtering, after filtering",
            "xlabel": "Time [ms]",
            "ylabel": "Voltage [mV]",
            "title": "Signal after filtering"
        }

        plot.my_plot(plotobject)

        plotobject = {
            "figure": 2,
            "data": [imported_data.data["Zeit"], imported_data.data["Kanal B"]],
            "savefig": "InputSignal" + "D" + Dehnung + "_No" + str(k),
            "legend": "T",
            "legendentries": "Applied Signal",
            "xlabel": "Time [ms]",
            "ylabel": "Voltage [V]",
            "title": "Input Signal"
        }

        plot.my_plot(plotobject)

        plotobject = {
            "figure": 3,
            "data": [imported_data.data["Zeit"], imported_data.data["Kanal A"]],
            "savefig": "Sensor" + "D" + Dehnung + "_No" + str(k),
            "legend": "T",
            "legendentries": "Voltage resistor",
            "xlabel": "Time [ms]",
            "ylabel": "Voltage [mV]",
            "title": "Voltage across measurement resistor"
        }

        plot.my_plot(plotobject)

        energy = CalculateEnergyOfSignal(filtered_signal)

        Peaks = sig.Segmentation_based_on_input_Signal(
            input_signal, list(CalculateEnergyOfSignal(energy)), False, k)

        # algorithm in order to find point where the value is lower than 13.5% of
        # the peak value
        fit_intervals = []

        for (i, item) in enumerate(Peaks):
            j = 0
            energy[item + j]
            try:
                while energy[item + j] > item * 0.135:
                    j = j + 1
            except Exception, e:
                pass

            fit_intervals.append([item, item + j])

        # calculate the decay constants from these intervals
        plt.close("all")

        for (i, item) in enumerate(fit_intervals):
            y = np.log(filtered_signal[item[0]:item[1]])
            x0 = np.array([-2, 1.0])
            x = imported_data.data["Zeit"][item[0]:item[1]]
            try:
                slope, intercept, r_value, p_value, std_err = stats.linregress(
                    x, y)
            except Exception, e:
                continue

            a = slope
            b = intercept

            # plotobject = {
            #     "figure": i,
            #     "data": [x, y],
            #     "legend": "T",
            #     "legendentries": "Logarithm_of_signal",
            #     "xlabel": "Time [ms]",
            #     "ylabel": "log[Voltage [mV]]",
            #     "title": "Fit for one decay time"
            # }

            # plot.my_plot(plotobject)

            # vecfunc = np.vectorize(func)

            # figurename = "Decay_Time_fit_" + "D" + \
            #     Dehnung + "_No" + str(k) + "_" + str(i)

            # plotobject = {
            #     "figure": i,
            #     "data": [x, vecfunc(x, a, b)],
            #     "savefig": figurename,
            #     "legend": "T",
            #     "legendentries": "fit",
            # }

            # plot.my_plot(plotobject)

            # take only the accurate fits
            if (r_value ** 2) > 0.98:
                tau.append(-1 / a)
                print "accepted"
            else:
                print "discarded"
            R_square.append(r_value ** 2)

    return tau
