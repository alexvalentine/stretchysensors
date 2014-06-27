import scipy as sc
import numpy as np
import csv
import sys
import argument_parser as argpars
import pandas as pd
sys.path.append("/Volumes/Daten/ds_Admin_Andreas/Studium/Vorlagen/Phyton")

# Possible options:
# - file: specifies the filename to export to, ex. "egg.csv"
# - header: does the file contain a header, ex. "T","F"
# - names: To be defined, if header is T, writes the names of the variables in the first row
# - data: data to store in the csv in case of export
#
# ------------------------------------------------------------------------
# Example usage:
# 	x = [5,1,2,3,4];
# y = pd.Series(data = x)
# z = np.ones((10,1))


# test_set = {
# 			"file":"test.csv",
# 			"header":"T",
# 			"data":[x,y,z],
# 			"names":["x","y","z"]
# 				}
#
# csvExport("-file test.csv -header F -data 5")
# csvExp.csvExport(test_set)

# also matrices can be stored just put them in row by row.

class csvExport:

    def __init__(self, arg):

    # parse all arguments into a telefon book:
        argparser = argpars.argument_parser()
        self.tel = argparser.read(arg)

        self.Export()

    def Export(self):
        self.file = self.tel["file"]
        self.header = self.tel["header"]
        self.data = self.tel["data"]

        csvfile = open(self.file, 'wb')
        spamwriter = csv.writer(csvfile, delimiter=",")

        if self.header == "T":

            self.names = self.tel["names"]
            spamwriter.writerow(self.names)

        max_length = self.determine_max_length()

        for i in xrange(0, max_length):

            row = []

            for j in self.data:

                if i < len(j):
                    if type(j[i]) is np.ndarray:
                        row.append(float(j[i]))
                    else:
                        row.append(j[i])

                else:
                    row.append("")

            spamwriter.writerow(row)

    def determine_max_length(self):

        max_length = 0

        for i in self.data:

            if max_length < len(i):
                max_length = len(i)

        return max_length

if __name__ == "__main__":

    print "main"
    # csvExport(test_set)
