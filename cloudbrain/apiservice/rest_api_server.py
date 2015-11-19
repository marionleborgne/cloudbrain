import time
import json
import random

from flask import Flask, request, current_app, abort
from flask.ext.cors import CORS
from functools import wraps
from cassandra.cluster import NoHostAvailable

from cloudbrain.utils.metadata_info import (map_metric_name_to_num_channels,
                                            get_supported_devices,
                                            get_metrics_names)
from cloudbrain.settings import WEBSERVER_PORT

_API_VERSION = "v1.0"

app = Flask(__name__)
CORS(app)
app.config['PROPAGATE_EXCEPTIONS'] = True

from cloudbrain.datastore.CassandraDAO import CassandraDAO


mock_data_enabled = False

try:
    dao = CassandraDAO()
    dao.connect()
    print "INFO: cassandra is running."
except NoHostAvailable:
    print "WARNING: cassandra is not running. Using mock data."
    mock_data_enabled = True



def support_jsonp(f):
    """Wraps JSONified output for JSONP"""


    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f()) + ')'
            return current_app.response_class(content,
                                              mimetype='application/json')
        else:
            return f(*args, **kwargs)


    return decorated_function



@app.route('/data', methods=['GET'])
@support_jsonp
def data():
    """
    GET metric data
    :return:
    """

    # return last 5 microseconds if start not specified.
    default_start_timestamp = int(time.time() * 1000000 - 5)
    device_id = request.args.get('device_id', None)
    device_name = request.args.get('device_name', None)
    metric = request.args.get('metric', None)
    start = int(request.args.get('start', default_start_timestamp))

    if not device_name:
        return "missing param: device_name", 500
    if not metric:
        return "missing param: metric", 500
    if not device_id:
        return "missing param: device_id", 500

    if mock_data_enabled:
        data_records = _get_mock_data(device_name, metric)
    else:
        data_records = _get_mock_data(device_name, metric) # temporary for demo
        #data_records = dao.get_data(device_name, device_id, metric, start)

    return json.dumps(data_records)



def _get_mock_data(device_name, metric):
    metric_to_num_channels = map_metric_name_to_num_channels(device_name)
    num_channels = metric_to_num_channels[metric]

    now = int(time.time() * 1000000 - 5)  # micro seconds

    data_records = []
    for i in xrange(5):
        record = {'timestamp': now + i}
        for j in xrange(num_channels):
            channel_name = 'channel_%s' % j
            record[channel_name] = random.random() * 10
        data_records.append(record)

    return data_records



@app.route('/api/%s/metadata/devices' %_API_VERSION, methods=['GET'])
@support_jsonp
def get_device_names():
    """ Returns the device names from the metadata file  """
    return json.dumps(get_supported_devices())



@app.route('/api/%s/users/<string:user_id>/devices' % _API_VERSION, methods=['GET'])
@support_jsonp
def get_registered_devices(user_id):
    """ Get the registered devices IDs for a user """
    return dao.get_registered_devices(user_id)



""" Tags """



def _generate_mock_tags(user_id, tag_name):
    if tag_name is None:
        tag_names = ["Facebook", "Netflix", "TechCrunch"]
    else:
        tag_names = [tag_name]

    tags = []
    for tag_name in tag_names:
        tags.append(
            {"tag_id": "c1f6e1f2-c964-48c0-8cdd-fafe8336190b",
             "user_id": user_id,
             "tag_name": tag_name,
             "metadata": {},
             "start": int(time.time() * 1000) - 10,
             "end": int(time.time() * 1000)
            })

    return tags



def generate_mock_tag(user_id, tag_id):
    tag = {"tag_id": tag_id,
           "user_id": user_id,
           "tag_name": "label_1",
           "metadata": {},
           "start": int(time.time() * 1000) - 10,
           "end": int(time.time() * 1000)
    }
    return tag



@app.route('/api/%s/users/<string:user_id>/tags' % _API_VERSION,
           methods=['GET'])
@support_jsonp
def get_tags(user_id):
    """Retrieve all tags for a specific user """

    tag_name = request.args.get('tag_name', None)

    if mock_data_enabled:
        tags = _generate_mock_tags(user_id, tag_name)
    else:
        tags = dao.get_tags(user_id, tag_name)

    return json.dumps(tags), 200



@app.route('/api/%s/users/<string:user_id>/tags/<string:tag_id>' % _API_VERSION,
           methods=['GET'])
@support_jsonp
def get_tag(user_id, tag_id):
    """Retrieve a specific tag for a specific user """

    if mock_data_enabled:
        tag = dao.get_mock_tag(user_id, tag_id)
    else:
        tag = dao.get_tag(user_id, tag_id)

    return json.dumps(tag), 200



@app.route('/api/%s/users/<string:user_id>/tags' % _API_VERSION,
           methods=['POST'])
@support_jsonp
def create_tag(user_id):
    if (not request.json
        or not 'tag_name' in request.json
        or not 'start' in request.json):
        abort(400)

    tag_name = request.json.get("tag_name")
    metadata = request.json.get("metadata")
    start = request.json.get("start")
    end = request.json.get("end")

    if mock_data_enabled:
        tag_id = "c1f6e1f2-c964-48c0-8cdd-fafe8336190b"
    else:
        tag_id = dao.create_tag(user_id, tag_name, metadata, start, end)

    return json.dumps({"tag_id": tag_id}), 500



""" Tag aggregates"""



def _generate_mock_tag_aggregates(user_id, tag_id, device_type, metrics):
    aggregates = []
    for metric in metrics:
        aggregates.append(
            {
                "aggregate_id": "c1f6e1f2-c964-48c0-8cdd-fafe83361977",
                "user_id": user_id,
                "tag_id": tag_id,
                "aggregate_type": "avg",
                "device_type": device_type,
                "aggregate_value": random.random() * 10,
                "metric": metric,
                "start": int(time.time() * 1000) - 10,
                "end": int(time.time() * 1000)
            })

    return aggregates



@app.route(('/api/%s/users/<string:user_id>/tags/<string:tag_id>/aggregates'
            % _API_VERSION), methods=['GET'])
@support_jsonp
def get_tag_aggregate(user_id, tag_id):
    """Retrieve all aggregates for a specific tag and user"""

    device_type = request.args.get('device_type', None)
    metrics = request.args.getlist('metrics', None)

    if device_type is None and len(metrics) == 0:
        device_types = get_supported_devices()
        for device_type in device_types:
            metrics.extend(get_metrics_names(device_type))
    elif len(metrics) == 0 and device_type is not None:
        metrics = get_metrics_names(device_type)
    elif len(metrics) > 0 and device_type is None:
        return "parameter 'device_type' is required to filter on `metrics`", 500

    if mock_data_enabled:
        aggregates = _generate_mock_tag_aggregates(user_id, tag_id, device_type, metrics)
    else:
        aggregates = dao.get_aggregates(user_id, tag_id, device_type, metrics)

    return json.dumps(aggregates), 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=WEBSERVER_PORT)
