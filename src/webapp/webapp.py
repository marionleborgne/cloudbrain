import redis
import logging
import simplejson as json
import sys
from msgpack import Unpacker
from flask import Flask, request, render_template, redirect
from daemon import runner
from os.path import dirname, abspath
from os import path
import msgpack

import csv


# add the shared settings file to namespace
sys.path.insert(0, dirname(dirname(abspath(__file__))))
import settings

REDIS_CONN = redis.StrictRedis(unix_socket_path=settings.REDIS_SOCKET_PATH)

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.route("/")
def index():
    return render_template('index.html'), 200

@app.route("/load_mock_data")
def load_mock_data():
    try:

        FULL_NAMESPACE = settings.FULL_NAMESPACE
        full_uniques = FULL_NAMESPACE + 'unique_metrics'
        r = redis.StrictRedis(unix_socket_path=settings.REDIS_SOCKET_PATH)
        pipe = r.pipeline()

        with open('/home/ubuntu/cloudbrain/src/webapp/static/data/data.json', 'rb') as jsonfile:
            data = json.load(jsonfile)
            for channel_data in data:
                values = channel_data['values']
                metric_name = channel_data['key']
                for value in values:
                    if values.index(value) < 1000:
                        datapoint = []
                        datapoint.append(value['x'])
                        datapoint.append(value['y'])


                        # Append to messagepack main namespace
                        key = ''.join((FULL_NAMESPACE, metric_name))
                        logger.info("key %s" % key)
                        pipe.append(key, msgpack.packb(datapoint))
                        pipe.sadd(full_uniques, key)
                        pipe.execute()

        return redirect("/")

    except Exception as e:
        error = "Error: " + repr(e)
        resp = json.dumps({'results': error})
        return resp, 500


@app.route("/flushall")
def flushall():
    try:
        REDIS_CONN.flushall()
        resp = json.dumps({'results' : 'Redis operation sucessfull. All keys have been flushed.'})
        return redirect("/")
    except Exception as e:
        error = "Error: " + e
        resp = json.dumps({'results': error})
        return resp, 500


@app.route("/metrics")
def metrics():
    try:
        unique_metrics = list(REDIS_CONN.smembers(settings.FULL_NAMESPACE + 'unique_metrics'))
        if not unique_metrics:
            resp = json.dumps({'results': 'Error: Could not retrieve list of unique metrics.'})
            return resp, 404
        else:
            metrics = [metric.replace(settings.FULL_NAMESPACE, "") for metric in unique_metrics]
            resp = json.dumps({'results': metrics})
            return resp, 200
    except Exception as e:
        error = "Error: " + e
        resp = json.dumps({'results': error})
        return resp, 500


@app.route("/app_settings")
def app_settings():

    app_settings = {'GRAPH_URL': settings.GRAPH_URL,
                    'OCULUS_HOST': settings.OCULUS_HOST,
                    'FULL_NAMESPACE': settings.FULL_NAMESPACE,
                    }

    resp = json.dumps(app_settings)
    return resp, 200


@app.route("/data", methods=['GET'])
def data():
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

    except Exception as e:
        error = "Error: " + e
        resp = json.dumps({'results': error})
        return resp, 500

@app.route("/anomalies", methods=['GET'])
def anomalies():
    try:
        filename = path.abspath(path.join(path.dirname(__file__), '..', settings.ANOMALY_DUMP))
        with open(filename, 'r') as f:
            raw_anomalies = f.read()
            anomalies = raw_anomalies.replace("handle_data", "").replace("(", "").replace(")","")
            resp = json.dumps({'results': anomalies})
            return resp, 200
    except Exception as e:
        error = "Error: " + e
        resp = json.dumps({'results': error})
        return resp, 500


class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = settings.LOG_PATH + '/webapp.log'
        self.stderr_path = settings.LOG_PATH + '/webapp.log'
        self.pidfile_path = settings.PID_PATH + '/webapp.pid'
        self.pidfile_timeout = 5

    def run(self):

        logger.info('starting webapp')
        logger.info('hosted at %s' % settings.WEBAPP_IP)
        logger.info('running on port %d' % settings.WEBAPP_PORT)

        app.run(settings.WEBAPP_IP, settings.WEBAPP_PORT)

if __name__ == "__main__":
    """
    Start the server
    """

    webapp = App()


    logger = logging.getLogger("AppLog")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s :: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    handler = logging.FileHandler(settings.LOG_PATH + '/webapp.log')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


    if len(sys.argv) > 1 and sys.argv[1] == 'run':
        webapp.run()
    else:
        daemon_runner = runner.DaemonRunner(webapp)
        daemon_runner.daemon_context.files_preserve = [handler.stream]
        daemon_runner.do_action()
