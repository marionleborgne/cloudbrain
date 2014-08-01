__author__ = 'marion'
import sys
import json
from os import path
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
import settings
import requests

import matplotlib.pyplot as plt
import numpy as np

filename = path.abspath(path.abspath(path.join(path.dirname(__file__), '..', settings.ANOMALY_DUMP)))

webapp_url = "http://localhost:1500/api?metric=%s"

f = open(filename, 'r')

jsonp_data = f.read()
json_data = jsonp_data.replace("handle_data(", "").replace(")", "")
anomalies = json.loads(json_data)

print anomalies


plt.figure()
for anomalie in anomalies:
    value = anomalie[0]
    name = anomalie[1]
    query = webapp_url % name
    r = requests.get(query)
    results = json.loads(r.content)
    points = results['results']

    x = [point[0] for point in points]
    nb_points = len(x)
    y = [point[1] for point in points]
    z = [value for point in points]

    plt.plot(x,y, label = "Metric Value")
    plt.plot(x,z, label = "Anomalie Threshold" )
    plt.title(name)
    plt.show()




