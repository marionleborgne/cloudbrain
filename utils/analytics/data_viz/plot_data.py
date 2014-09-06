__author__ = 'marion'

import csv
import matplotlib.pyplot as plt

def getColumn(filename, column):
    results = csv.reader(open(filename, 'r'))
    return [result[column] for result in results]


data_file = "../data/jim_10filt.csv"

time = getColumn(data_file,8)
channel_0 = getColumn(data_file,0)

plt.figure("Time/channel_0")
plt.xlabel("Time")
plt.ylabel("channel_0")
plt.plot(time,channel_0)