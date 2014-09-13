__author__ = 'marion'

import csv
import json
import matplotlib.pyplot as plt

'''
with open('../../../src/webapp/static/data/eeg_mock_data.json', 'rb') as jsonfile:
    data = json.load(jsonfile)

'''


with open('../../../src/webapp/static/data/jim_10filt.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    all_channels_data = []
    for k in xrange(8):
        data = {}
        data['key'] = "channel-%d" %k
        data['values'] =[]
        all_channels_data.append(data)

    row_count = 0
    for row in reader:
        for i in xrange(8):
            if len(row) > 8:
                value = {}
                value['x'] = row_count
                value['y'] = row[i]
                all_channels_data[i]['values'].append(value)
        row_count = row_count + 1

json_data = json.dumps(all_channels_data)


file = open('../../../src/webapp/static/data/eeg_mock_data.json','w')
file.write(json_data)
file.close()
'''
plt.figure("Time/channel_0")
plt.xlabel("Time")
plt.ylabel("channel_0")
plt.plot(time,channel_0)
'''