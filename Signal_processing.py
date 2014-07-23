import matplotlib.pylab as plt
import numpy as np
from scipy.signal import butter, lfilter, filtfilt, firwin
from scipy.optimize import curve_fit
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})


import sys
sys.path.append("/Volumes/Daten/ds_Admin_Andreas/Studium/Vorlagen/Phyton")


import csvImport as csvImp
# import csvExport as csvExp
import my_plot as plot
from operator import itemgetter

# signal processing


def CalculateEnergyOfSignal(signal):

    for x in xrange(10, len(signal)):
        signal[x] = signal[x] ** 2

    return signal


def PeakDetection(signal, plot_it=False, number=0):
        # input: signal as 1D array, important to prefilter it, number is the number of the plot.
        # output: array with the indices where peaks were found.
        #
        # Main Idea:
        #  -    First remove the noise, by taking the average of the signal and adding a safety factor to it.
        #  -    Then take find the intervals, where the signal is above this threshold
        #  -    Then find the maximum in this signal
        #  -    Plot the maximum and the signal to verify that the peaks were detected correctly.
        threshold = np.mean(signal) * 3
        test = []
        # this function stores the beginning and the end of an interval that
        # contains the peak maximum in a nested list
        intervals = []

        beginning = False
        start = 0

        # detect the intervals, where the signal is above threshold.

        for (i, item) in enumerate(signal):

            if (threshold < item):

                if not beginning:
                    beginning = True
                    start = i
                test.append(0)

            else:
                if beginning:
                    beginning = False
                    intervals.append([start, i])

                test.append(1)

        # find the maximum in the intervals
        indices_peaks = []

        for (i, item) in enumerate(intervals):
            max_idx, max_val = max(
                enumerate(signal[item[0]:item[1]]), key=operator.itemgetter(1))
            indices_peaks.append(max_idx + item[0])

        if plot_it == True:

            plotobject = {
                "figure": 100,
                "data": [indices_peaks, signal[indices_peaks]],
                "marker": "+",
                "legend": "T",
                "legendentries": "Detected peaks",
                "linestyle": "None"
            }

            plot.my_plot(plotobject)

            plotobject = {
                "figure": 100,
                "data": [xrange(0, len(signal)), signal],
                "savefig": "Peak_detection" + str(number),
                "legend": "T",
                "legendentries": "original signal",
                "xlabel": "Time",
                "ylabel": "SignalEnergy",
                "title": "Detected Peaks"
            }

            plot.my_plot(plotobject)

        return indices_peaks


def Segmentation_based_on_input_Signal(inputsignal, signal, plot_it=False, number=0):
    # this function does a segmentation based on an applied inputsignal
    # input
    # - inputsignal: squarewave
    # - signal: signal to segment
    # output:
    # - location of the detected maxima

    zerocrossing = np.where(np.diff(np.sign(inputsignal)))[0]

    zerocrossing = list(zerocrossing)

    # detect the maxima in the decays

    intervals = []

    for x in xrange(1, len(zerocrossing) - 1):
        intervals.append([zerocrossing[x], zerocrossing[x + 1]])

    indices_peaks = []

    for (i, item) in enumerate(intervals):

        max_idx = signal[item[0]:item[1]].index(max(
            signal[item[0]:item[1]]))
        indices_peaks.append(int(max_idx + item[0]))

    peaks = []

    for (i, item) in enumerate(indices_peaks):
        peaks.append(signal[item])

    if plot_it == True:

            plotobject = {
                "figure": 100,
                "data": [indices_peaks, peaks],
                "marker": "+",
                "legend": "T",
                "legendentries": "Detected peaks",
                "linestyle": "None"
            }

            plot.my_plot(plotobject)

            plotobject = {
                "figure": 100,
                "data": [xrange(0, len(signal)), signal],
                "savefig": "Peak_detection" + str(number),
                "legend": "T",
                "legendentries": "original signal",
                "xlabel": "Time",
                "ylabel": "SignalEnergy",
                "title": "Detected Peaks"
            }

            plot.my_plot(plotobject)

    return indices_peaks

# How to overlay to signals automatically:

a = [0, 0, 0, 0, 0, 1, 1, 0, 0]
b = [0, 0, 1, 1, 0, 0, 0, 0, 0]
corr = np.correlate(a, b, "full")
maxim = corr.argmax() - len(b)

plt.plot(x, a)
plt.plot(x + x[maxim], b)


if __name__ == "__main__":
    print "main"
