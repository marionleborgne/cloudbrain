__author__ = 'marion'

import urllib2
import simplejson

metric = "channel-3"

url = "http://localhost:1500/api?metric=%s" % metric

headers = { 'Content-Type' : 'application/json' }
req = urllib2.Request(url, headers=headers)

opener = urllib2.build_opener()
f = opener.open(req)
raw_result = simplejson.load(f)
results = raw_result['results']

print "metric : %s  |  timestamp : %s  | datapoint : %s" %(metric, results[0][0], results[0][1])