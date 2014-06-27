import scipy as sc
import numpy as np
import csv
import sys
import argument_parser as argpars
import pandas as pd
sys.path.append("/Volumes/Daten/ds_Admin_Andreas/Studium/Vorlagen/Phyton")

# This documentation is not up to date yet...

# Possible options:
# - file: specifies the filename to export to, ex. "egg.csv"
# - header: does the file contain a header, ex. "T","F"
# - names: names of the variables if there is no header
# - HasUnits: if true, the second line contains the units of the variables
# - Units: List containing the units of the variables if they are not in the csv file
# ------------------------------------------------------------------------
# Example usage:

# test_set = {
# 			"file":"test.csv",
# 			"header":"T",
# 			if header is not true then the names of the variables can be specified
# 			"names":["x","y","z"]
# 			"HasUnits":"T",
# 			"Units":["[m]","[s]","[kg/s]"]
# 			"LinesToSkip":[2] //list that contains the lines that should be skipped in the analysis
# 			"PrintContent":"T" // prints the content
# 				}
#
# csvImport(test_set)
#
# external example usage:
# test_set = {
    #     "file": 'Rm1000Rs1000Cs22.csv',
    #     "header": "F",
    # if header is not true then the names of the variables can
    # be specified
    #     "names": ["index", "tau", "Capa", "Resistance", "Time"],
    #     "HasUnits": "F",
    #     "LinesToSkip": [],
    #     "PrintContent": "T"
    # }

    # test = csvImp.csvImport(test_set)

    # print test.data["tau"]

# Output:
# - data: dictionary containing the data as np arrays
# - Units: list containing the units of the data
# - counter: number of rows in the csv
#
# test_set = {
#     "file": filename,
#     "header": "F",
#     "names": ["index", "tau", "Capa", "Resistance", "Time"],
#     "HasUnits": "F",
#     "LinesToSkip": [],
#     "PrintContent": "F"
# }

# test = csvImp.csvImport(test_set)


# My importer is just crab....
# use the pandas library instead.... Can also skip lines etc...
#   data = pd.read_csv("data_for_boxplot.csv", names=["a", "b", "c", "d"])

class csvImport:

    def __init__(self, arg):

    # parse all arguments into a telefon book:
        argparser = argpars.argument_parser()
        self.tel = argparser.read(arg)

        self.Import()

    def Import(self):

        self.file = self.tel["file"]
        self.header = self.tel["header"]

        if "LinesToSkip" in self.tel.keys():
            self.LinesToSkip = self.tel["LinesToSkip"]
            print(self.LinesToSkip)
        else:
            self.LinesToSkip = []
        # This variable counts the rows the csv file
        self.counter = 0
        #  empty dictionary in order to store the data
        self.data = {}

        with open(self.file, 'rU') as f:

            reader = csv.reader(f)

            # read the header
            if self.header == "T":
                self.names = []
                j = 0
                for item in next(reader):
                    self.names.append(item)
                    self.data[item] = []
                    j = j + 1
                self.counter = self.counter + 1
            else:
                self.names = self.tel["names"]
                for item in self.names:
                    self.data[item] = []

            # read the units
            if "HasUnits" in self.tel.keys():
                self.HasUnits = self.tel["HasUnits"]
                if self.HasUnits == "T":
                    self.Units = []

                    for item in next(reader):
                        self.Units.append(item)
                    self.counter = self.counter + 1
                else:
                    self.names = self.tel["names"]

            # loop through the data and convert it to float, skip the lines
            # that are in the list Lines to Skip

            for row in reader:
                i = 0

                if self.counter not in self.LinesToSkip:

                    for item in row:
                        try:
                            self.data[self.names[i]].append(float(item))
                            i = i + 1
                        except Exception, e:
                            pass

                else:
                    print("Skipped Lines " + str(self.counter))

                self.counter = self.counter + 1

            if "PrintContent" in self.tel.keys():
                if self.tel["PrintContent"] == "T":
                    with open(self.file) as f:
                        reader = csv.reader(f, 'rU')
                        for row in reader:
                            print(row)

        # convert the list objects to numpy arrays
        for data in self.data.keys():
            self.data[data] = np.array(self.data[data])

if __name__ == "__main__":

    print("main")
    test_set = {
        "file": '1_MO_220pF_1MO_1MO_A_V1MO_B_SIG_F_200Hz_13.csv',
        "header": "T",
        # if header is not true then the names of the variables can
        # be specified
        "names": ["x", "y", "z"],
        "HasUnits": "T",
                    "Units": ["[m]", "[s]", "[kg/s]"],
                    "LinesToSkip": [2],
                    "PrintContent": "F"
    }

    test = csvImport(test_set)

    print(test.data)
    print(test.Units)
