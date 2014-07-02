__author__ = 'marion'
import requests
import json
import msgpack
import socket
import sys
from os.path import dirname, abspath
import redis
import time

# add the shared settings file to namespace
sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
import settings


class NoDataException(Exception):
    pass


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ims_url = "http://ims.us-east-1.cloudweaverdiscovery.com:8080/ims/tenants/T347/metrics"
headers = {'content-type' : 'application/json'}

print 'Loading data over UDP via Horizon...'
metric_set = 'unique_metrics'

#resourceId = "N347-f"
#metric = 'lastmin'
limit = ''
timescale = '10'
aggregate = 'avg'

f = open("metrics.json", 'r')

metrics = json.loads(f.read())

while True:
    for metric in metrics:

        if metrics[metric]["type"] == "NODE" and not metrics[metric]["requiresExtra"]:

            nodes = ["N347-f"] # AlarmManager

            for nodeId in nodes:

                payload = [{"aggregate": aggregate, "resourceId": nodeId, "metric": metric, "limit": limit, "timescale": timescale}]
                print "payload : %s" % json.dumps(payload)
                r = requests.post(ims_url, data=json.dumps(payload), headers=headers)
                results = json.loads(r.content)
                print  "==> Results for metric '%s' : %s" % (metric, str(results))

                for result in results:
                    if len(result) > 0:
                        datapoints = result['points']
                        metric = result['metric']
                        for datapoint in datapoints:
                            packet = msgpack.packb((metric, datapoint))
                            sock.sendto(packet, ("localhost", settings.UDP_PORT))

                        print "Connecting to Redis..."
                        r = redis.StrictRedis(unix_socket_path=settings.REDIS_SOCKET_PATH)
                        time.sleep(5)

                        try:
                            x = r.smembers(settings.FULL_NAMESPACE + metric_set)
                            if x is None:
                                raise NoDataException

                            x = r.get(settings.FULL_NAMESPACE + metric)
                            if x is None:
                                raise NoDataException

                            print "Congratulations! The data made it in. The Horizon pipeline seems to be working."

                        except NoDataException:
                            print "Woops, looks like the metrics didn't make it into Horizon. Try again?"

    time.sleep(30)
