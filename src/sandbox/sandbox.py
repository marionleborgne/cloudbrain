import logging
from Queue import Empty
from redis import StrictRedis
from time import time, sleep
from threading import Thread
from collections import defaultdict
from multiprocessing import Process, Manager, Queue
from msgpack import Unpacker, unpackb, packb
from os import path, kill, getpid, system
from math import ceil
import traceback
import operator
import socket
import sys
from os.path import dirname, abspath
import time
import math
import msgpack

sys.path.insert(0, dirname(dirname(abspath(__file__))))
import settings
import redis

sys.path.insert(0, dirname(dirname(abspath(__file__))) + "/analyzer")
from alerters import trigger_alert
from algorithms import run_selected_algorithm
from algorithm_exceptions import *
import json

logger = logging.getLogger("AnalyzerLog")


class Analyzer(Thread):
    def __init__(self, parent_pid):
        """
        Initialize the Analyzer
        """
        super(Analyzer, self).__init__()
        self.redis_conn = StrictRedis(unix_socket_path = settings.REDIS_SOCKET_PATH)
        self.daemon = True
        self.parent_pid = parent_pid
        self.current_pid = getpid()
        self.anomalous_metrics = Manager().list()
        self.exceptions_q = Queue()
        self.anomaly_breakdown_q = Queue()

    def check_if_parent_is_alive(self):
        """
        Self explanatory
        """
        try:
            kill(self.current_pid, 0)
            kill(self.parent_pid, 0)
        except:
            exit(0)

    def send_graphite_metric(self, name, value):
        if settings.GRAPHITE_HOST != '':
            sock = socket.socket()
            sock.connect((settings.GRAPHITE_HOST, settings.CARBON_PORT))
            sock.sendall('%s %s %i\n' % (name, value, time()))
            sock.close()
            return True

        return False

    def spin_process(self, i, unique_metrics):
        """
        Assign a bunch of metrics for a process to analyze.
        """
        # Discover assigned metrics
        keys_per_processor = int(ceil(float(len(unique_metrics)) / float(settings.ANALYZER_PROCESSES)))
        if i == settings.ANALYZER_PROCESSES:
            assigned_max = len(unique_metrics)
        else:
            assigned_max = i * keys_per_processor
        assigned_min = assigned_max - keys_per_processor
        assigned_keys = range(assigned_min, assigned_max)

        # Compile assigned metrics
        assigned_metrics = [unique_metrics[index] for index in assigned_keys]

        # Check if this process is unnecessary
        if len(assigned_metrics) == 0:
            return

        # Multi get series
        raw_assigned = self.redis_conn.mget(assigned_metrics)

        # Make process-specific dicts
        exceptions = defaultdict(int)
        anomaly_breakdown = defaultdict(int)

        # Distill timeseries strings into lists
        for i, metric_name in enumerate(assigned_metrics):
            self.check_if_parent_is_alive()

            try:
                raw_series = raw_assigned[i]
                unpacker = Unpacker(use_list = False)
                unpacker.feed(raw_series)
                timeseries = list(unpacker)

                anomalous, ensemble, datapoint = run_selected_algorithm(timeseries, metric_name)

                # If it's anomalous, add it to list
                if anomalous:
                    base_name = metric_name.replace(settings.FULL_NAMESPACE, '', 1)
                    metric = [datapoint, base_name]
                    self.anomalous_metrics.append(metric)

                    # Get the anomaly breakdown - who returned True?
                    for index, value in enumerate(ensemble):
                        if value:
                            algorithm = settings.ALGORITHMS[index]
                            anomaly_breakdown[algorithm] += 1

            # It could have been deleted by the Roomba
            except TypeError:
                exceptions['DeletedByRoomba'] += 1
            except TooShort:
                exceptions['TooShort'] += 1
            except Stale:
                exceptions['Stale'] += 1
            except Boring:
                exceptions['Boring'] += 1
            except:
                exceptions['Other'] += 1
                logger.info(traceback.format_exc())

        # Add values to the queue so the parent process can collate
        for key, value in anomaly_breakdown.items():
            self.anomaly_breakdown_q.put((key, value))

        for key, value in exceptions.items():
            self.exceptions_q.put((key, value))

    def test(self):
        """
        Called when the process intializes.
        """
        while 1:
            now = time()

            # Make sure Redis is up
            try:
                self.redis_conn.ping()
            except:
                logger.error('cloudbrain can\'t connect to redis at socket path %s' % settings.REDIS_SOCKET_PATH)
                sleep(10)
                self.redis_conn = StrictRedis(unix_socket_path = settings.REDIS_SOCKET_PATH)
                continue

            # Discover unique metrics
            unique_metrics = list(self.redis_conn.smembers(settings.FULL_NAMESPACE + 'unique_metrics'))

            if len(unique_metrics) == 0:
                logger.info('no metrics in redis. try adding some - see README')
                sleep(10)
                continue

            # Spawn processes
            pids = []
            for i in range(1, settings.ANALYZER_PROCESSES + 1):
                if i > len(unique_metrics):
                    logger.info('WARNING: cloudbrain is set for more cores than needed.')
                    break

                p = Process(target=self.spin_process, args=(i, unique_metrics))
                pids.append(p)
                p.start()

            # Send wait signal to zombie processes
            for p in pids:
                p.join()

            # Grab data from the queue and populate dictionaries
            exceptions = dict()
            anomaly_breakdown = dict()
            while 1:
                try:
                    key, value = self.anomaly_breakdown_q.get_nowait()
                    if key not in anomaly_breakdown.keys():
                        anomaly_breakdown[key] = value
                    else:
                        anomaly_breakdown[key] += value
                except Empty:
                    break

            while 1:
                try:
                    key, value = self.exceptions_q.get_nowait()
                    if key not in exceptions.keys():
                        exceptions[key] = value
                    else:
                        exceptions[key] += value
                except Empty:
                    break

            # Send alerts
            if settings.ENABLE_ALERTS:
                for alert in settings.ALERTS:
                    for metric in self.anomalous_metrics:
                        if alert[0] in metric[1]:
                            cache_key = 'last_alert.%s.%s' % (alert[1], metric[1])
                            try:
                                last_alert = self.redis_conn.get(cache_key)
                                if not last_alert:
                                    self.redis_conn.setex(cache_key, alert[2], packb(metric[0]))
                                    trigger_alert(alert, metric)

                            except Exception as e:
                                logger.error("couldn't send alert: %s" % e)

            # Write anomalous_metrics to static webapp directory
            filename = path.abspath(path.join(path.dirname(__file__), '..', settings.ANOMALY_DUMP))
            with open(filename, 'w') as fh:
                # Make it JSONP with a handle_data() function
                anomalous_metrics = list(self.anomalous_metrics)
                anomalous_metrics.sort(key=operator.itemgetter(1))
                fh.write('handle_data(%s)' % anomalous_metrics)

            # Log progress
            logger.info('seconds to run    :: %.2f' % (time() - now))
            logger.info('total metrics     :: %d' % len(unique_metrics))
            logger.info('total analyzed    :: %d' % (len(unique_metrics) - sum(exceptions.values())))
            logger.info('total anomalies   :: %d' % len(self.anomalous_metrics))
            logger.info('exception stats   :: %s' % exceptions)
            logger.info('anomaly breakdown :: %s' % anomaly_breakdown)

            # Log to Graphite
            self.send_graphite_metric('cloudbrain.analyzer.run_time', '%.2f' % (time() - now))
            self.send_graphite_metric('cloudbrain.analyzer.total_analyzed', '%.2f' % (len(unique_metrics) - sum(exceptions.values())))

            # Check canary metric
            raw_series = self.redis_conn.get(settings.FULL_NAMESPACE + settings.CANARY_METRIC)
            if raw_series is not None:
                unpacker = Unpacker(use_list = False)
                unpacker.feed(raw_series)
                timeseries = list(unpacker)
                time_human = (timeseries[-1][0] - timeseries[0][0]) / 3600
                projected = 24 * (time() - now) / time_human

                logger.info('canary duration   :: %.2f' % time_human)
                self.send_graphite_metric('cloudbrain.analyzer.duration', '%.2f' % time_human)
                self.send_graphite_metric('cloudbrain.analyzer.projected', '%.2f' % projected)

            # Reset counters
            self.anomalous_metrics[:] = []

            # Sleep if it went too fast
            if time() - now < 5:
                logger.info('sleeping due to low run time...')
                sleep(10)

REDIS_CONN = redis.StrictRedis(unix_socket_path=settings.REDIS_SOCKET_PATH)

def test2():
    unique_metrics = list(REDIS_CONN.smembers(settings.FULL_NAMESPACE + 'unique_metrics'))
    resp = json.dumps({'results': unique_metrics})
    return resp, 200

def test3():
    start = 0
    end = 10

    metric = "marion.channel-0"

    raw_series = REDIS_CONN.get(settings.FULL_NAMESPACE + metric)
    if not raw_series:
        resp = json.dumps({'results': 'Error: No metric by that name'})
        return resp, 404
    else:
        unpacker = Unpacker(use_list = False)
        unpacker.feed(raw_series)
        timeseries = []

        point = {'x':datapoint[0],'y':datapoint[1]}

        if (start is None) and (end is not None):
            for datapoint in unpacker:
                if datapoint[0] < int(end):
                    timeseries.append(point)
        elif (start is not None) and (end is None):
            for datapoint in unpacker:
                if datapoint[0] > int(start):
                    timeseries.append(point)
        elif (start is not None) and (end is not None):
            for datapoint in unpacker:
                if (datapoint[0] > int(start)) and (datapoint[0] < int(end)):
                    timeseries.append(point)
        elif (start is None) and (end is None):
            timeseries = [{'x':datapoint[0],'y':datapoint[1]} for datapoint in unpacker]

        resp = json.dumps({'results': timeseries})
        return resp, 200

def api():
    metric = request.args.get('metric', None)
    start = request.args.get('start', None)
    end = request.args.get('end', None)

    if metric is None:
        metrics = ['channel-0', 'channel-1', 'channel-2', 'channel-3', 'channel-4', 'channel-5', 'channel-6', 'channel-7']
    else:
        metrics = [metric]

    try:
        all_channels_data = []
        for metric in metrics:

            single_channel_data = {}

            raw_series = REDIS_CONN.get(settings.FULL_NAMESPACE + metric)
            if not raw_series:
                resp = json.dumps({'results': 'Error: No metric by that name'})
                return resp, 404
            else:
                unpacker = Unpacker(use_list = False)
                unpacker.feed(raw_series)
                timeseries = []

                if (start is None) and (end is not None):
                    for datapoint in unpacker:
                        if datapoint[0] < int(end):
                            point = {'x' : datapoint[0], 'y':datapoint[1]}
                            timeseries.append(point)
                elif (start is not None) and (end is None):
                    for datapoint in unpacker:
                        if datapoint[0] > int(start):
                            point = {'x' : datapoint[0], 'y':datapoint[1]}
                            timeseries.append(point)
                elif (start is not None) and (end is not None):
                    for datapoint in unpacker:
                        if (datapoint[0] > int(start)) and (datapoint[0] < int(end)):
                            point = {'x' : datapoint[0], 'y':datapoint[1]}
                            timeseries.append(point)
                elif (start is None) and (end is None):
                    timeseries = [{'x' : datapoint[0], 'y':datapoint[1]} for datapoint in unpacker]

                single_channel_data['key'] = metric
                single_channel_data['values'] = timeseries
                all_channels_data.append(single_channel_data)

        resp = json.dumps({'results': all_channels_data})
        return resp, 200

    except Exception as e:
        error = "Error: " + e
        resp = json.dumps({'results': error})
        return resp, 500

def stream_mock_data():

        FULL_NAMESPACE = settings.FULL_NAMESPACE
        MINI_NAMESPACE = settings.MINI_NAMESPACE
        MAX_RESOLUTION = settings.MAX_RESOLUTION
        full_uniques = FULL_NAMESPACE + 'unique_metrics'
        mini_uniques = MINI_NAMESPACE + 'unique_metrics'
        r = redis.StrictRedis(unix_socket_path=settings.REDIS_SOCKET_PATH)
        pipe = r.pipeline()

        metric = 'channel-%s'
        metric_set = 'unique_metrics'

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        nbPoints = 3600
        end = int(time.time())
        start = int(end - nbPoints)

        for k in xrange(7):
            print k
            for i in xrange(start, end):
                datapoint = []
                datapoint.append(i)

                value = 50 + math.sin(i*k * 0.001)

                datapoint.append(value)

                metric_name = metric % k

                '''
                packet = msgpack.packb((metric_name, datapoint))
                sock.sendto(packet, ('localhost', settings.UDP_PORT))
                '''

                # Append to messagepack main namespace
                key = ''.join((FULL_NAMESPACE, metric_name))
                logger.info("key %s" % key)
                pipe.append(key, msgpack.packb(datapoint))
                pipe.sadd(full_uniques, key)


                pipe.execute()




if __name__ == '__main__':
    #a = Analyzer(getpid())
    #a.test()
    resp = stream_mock_data()
    print resp