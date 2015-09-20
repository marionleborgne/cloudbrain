import time
import json
import random
import uuid
from flask import Flask, request, current_app, abort
from functools import wraps
from cloudbrain.utils.metadata_info import map_metric_name_to_num_channels, get_supported_devices
from cloudbrain.settings import WEBSERVER_PORT

_MOCK_ENABLED = True
_API_VERSION = "v1.0"

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

if not _MOCK_ENABLED:
  from cloudbrain.datastore.CassandraDAO import CassandraDAO

  dao = CassandraDAO()
  dao.connect()


def support_jsonp(f):
  """Wraps JSONified output for JSONP"""

  @wraps(f)
  def decorated_function(*args, **kwargs):
    callback = request.args.get('callback', False)
    if callback:
      content = str(callback) + '(' + str(f()) + ')'
      return current_app.response_class(content, mimetype='application/json')
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

  default_start_timestamp = int(time.time() * 1000000 - 5)  # return last 5 microseconds if start not specified.
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

  if _MOCK_ENABLED:
    data_records = _get_mock_data(device_name, metric)
  else:
    data_records = dao.get_data(device_name, device_id, metric, start)

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


@app.route('/metadata/devices', methods=['GET'])
@support_jsonp
def get_device_names():
  """ Returns the device names from the metadata file  """
  return json.dumps(get_supported_devices())


@app.route('/registered_devices', methods=['GET'])
@support_jsonp
def get_registered_devices():
  """ Get the registered devices IDs """
  if _MOCK_ENABLED:
    registered_devices = ['octopicorn']  # mock ID
  else:
    registered_devices = dao.get_registered_devices()
  return json.dumps(registered_devices)


@app.route('/api/%s/tags' % _API_VERSION, methods=['GET'])
@support_jsonp
def get_tags():
  """Retrieve all tags"""
  if _MOCK_ENABLED:
    tags = [
      {"tag_id": "c1f6e1f2-c964-48c0-8cdd-fafe8336190b",
       "user_id": "octopicorn",
       "tag_name": "label1",
       "metadata": {},
       "start": int(time.time() * 1000),
       "end": int(time.time() * 1000)
      },
      {"tag_id": "c1f6e1f2-c964-48c0-8cdd-fafe83361977",
       "user_id": "octopicorn",
       "tag_name": "label2",
       "metadata": {},
       "start": int(time.time() * 1000),
       "end": int(time.time() * 1000)
      }
    ]
  else:
    tags = dao.get_tags()

  return json.dumps(tags), 200


@app.route('/api/%s/tags/<string:tag_id>' % _API_VERSION, methods=['GET'])
@support_jsonp
def get_tag(tag_id):
  """Retrieve a specific tag """

  if _MOCK_ENABLED:
    tag = {"tag_id": tag_id,
           "user_id": "octopicorn",
           "tag_name": "label1",
           "metadata": {},
           "start": int(time.time() * 1000),
           "end": int(time.time() * 1000)
    }
  else:
    tag = dao.get_tag(tag_id)

  return json.dumps(tag), 200


@app.route('/api/%s/tags' % _API_VERSION, methods=['POST'])
@support_jsonp
def create_tag():
  if (not request.json
      or not 'user_id' in request.json
      or not 'tag_name' in request.json
      or not 'start' in request.json):
    abort(400)

  user_id = request.json.get("user_id")
  tag_name = request.json.get("tag_name")
  metadata = request.json.get("metadata")
  start = request.json.get("start")
  end = request.json.get("end")

  if _MOCK_ENABLED:
    tag_id = "c1f6e1f2-c964-48c0-8cdd-fafe8336190b"
  else:
    tag_id = dao.create_tag(user_id, tag_name, metadata, start, end)

  return json.dumps(tag_id), 500


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=WEBSERVER_PORT)
