import matplotlib.pylab as plt
import numpy as np
from scipy.signal import butter, lfilter, filtfilt, firwin
from scipy.optimize import curve_fit
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})


import sys
sys.path.append("\\vfiler1.seas.harvard.edu\group0\jlewis\User Files\Valentine")


import csvImport as csvImp
# import csvExport as csvExp
import my_plot as plot

#POOP TEST

# from this file, generate a Template for later work!!!
def func(x, a, b):
    return a * x + b

if __name__ == "__main__":

    test_set = {
        "file": '1_MO_220pF_1MO_1MO_A_V1MO_B_SIG_F_200Hz_13.csv',
        "header": "T",
        # if header is not true then the names of the variables can bespecified
        "names": ["x", "y", "z"],
        "HasUnits": "T",
        "Units": ["[m]", "[s]", "[kg/s]"],
        "LinesToSkip": [2],
        "PrintContent": "F"
    }

    imported_data = csvImp.csvImport(test_set)

    # Have to do a peak detection, skip the first and last entry and then fit
    # an exponential to the data, extract the different RC time constants and
    # average, make a boxplot of the result.

    # detect the zero crossings in the square wave signal
    zerocrossing = np.where(
        np.diff(np.sign(imported_data.data["Channel B"])))[0]
    print(zerocrossing)
    # calculate the width of the peak finder as the difference of the second
    # and third entry in the zerocrossing vector.

    timepoints_of_zerocrossing = imported_data.data["Time"][zerocrossing]

    # filter the signal
    N = 10
    Fc = 1000
    Fs = 1600
    # provide them to firwin
    h = firwin(numtaps=N, cutoff=40, nyq=Fs / 2)

    # 'x' is the time-series data you are filtering
    filtered_signal = lfilter(h, 1.0, imported_data.data["Channel A"])

    # use the zerocrossing in order to segment the signal

    segment = filtered_signal[zerocrossing[0]:zerocrossing[1]]

    maximum = np.argmax(segment)

    processed_segment = np.log(filtered_signal[maximum:zerocrossing[1]])

    x0 = np.array([-2, 1.0])
    x = imported_data.data["Time"][maximum:zerocrossing[1]]

    x = x[0:600]
    y = processed_segment[0:600]
    para = curve_fit(func, x, y, x0, sigma=None)
    a = para[0][0]
    b = para[0][1]
    # popt, pcov= curve_fit(func, ,processed_segment, x0,sigma = None)

    # print popt

    plotobject = {
        "figure": 1,
        "data": [timepoints_of_zerocrossing, [100] * len(timepoints_of_zerocrossing)],
        "marker": "+",
        "legend": "T",
        "legendentries": "zero crossing",
        "linestyle": "None"
    }

    plot.my_plot(plotobject)

    plotobject = {
        "figure": 1,
        "data": [imported_data.data["Time"], imported_data.data["Channel A"], filtered_signal],
        "savefig": "test",
        "legend": "T",
        "legendentries": "before filtering, after filtering",
        "xlabel": "test",
        "ylabel": "test",
        "title": "test"
    }

    plot.my_plot(plotobject)

    plotobject = {
        "figure": 2,
        "data": [imported_data.data["Time"][maximum:zerocrossing[1]], processed_segment],
        "savefig": "test",
        "legend": "T",
        "legendentries": "before filtering, after filtering",
        "xlabel": "test",
        "ylabel": "test",
        "title": "test"
    }

    plot.my_plot(plotobject)

    vecfunc = np.vectorize(func)

    print(vecfunc(x, a, b))

    plotobject = {
        "figure": 2,
        "data": [x, vecfunc(x, a, b)],
        "savefig": "test",
        "legend": "T",
        "legendentries": "fit",
        "xlabel": "test",
        "ylabel": "test",
        "title": "test"
    }

    plot.my_plot(plotobject)

    #  time constant in seconds
    print(-1 / a / 1000)

    print(zerocrossing)

