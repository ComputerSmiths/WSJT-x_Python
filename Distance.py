#!/usr/bin/env python3
#
# Calculate distance (by year?) from wsjtx.log
#
# rev 1.0 06/09/2021 WPNS read and parse file
# rev 1.1 06/09/2021 WPNS parse yar, accumulate by year.

import time
from datetime import datetime
from pyhamtools.locator import calculate_distance

QSOfile = open("wsjtx.log","r")

LineCount = 0
DistanceAcc = 0
StartYear = 2015
MyGrid = "FN21xb90"
DistanceAcc = [0]*10  # allow for 10 years

for line in QSOfile:
    Values = line.split(",")
    try:
        Year = int(Values[0][0:4])
    except:
        continue
    Grid = Values[5]
    if (Grid != ''):
        try:
            Distance = calculate_distance(MyGrid, Grid)
            DistanceAcc[Year-StartYear] += Distance
        except:
            continue
    LineCount += 1
QSOfile.close()

print("Found {} valid lines in file".format(LineCount))

for year in range(len(DistanceAcc)):
    if DistanceAcc[year] > 0:
        print ("{} {}".format(year+StartYear,int(DistanceAcc[year])))
