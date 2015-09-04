import time
import json
import random
from flask import Flask, request, current_app
from functools import wraps
from cloudbrain.utils.metadata_info import map_metric_name_to_num_channels, get_supported_devices
from cloudbrain.settings import WEBSERVER_PORT

_MOCK_ENABLED = True


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

if not _MOCK_ENABLED:
  from cloudbrain.datastore.CassandraDAL import CassandraDAL
  dao = CassandraDAL()
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

  default_start_timestamp = int(time.time() * 1000000 - 5)# return last 5 microseconds if start not specified.
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


@app.route('/power_bands', methods=['GET'])
@support_jsonp
def power_bands():
  """
  GET the power bands data
  :return:
  """

  default_start_timestamp = int(time.time() * 1000000 - 5)# return last 5 microseconds if start not specified.
  device_id = request.args.get('device_id', None)
  device_name = request.args.get('device_name', None)
  start = int(request.args.get('start', default_start_timestamp))

  if not device_name:
    return "missing param: device_name", 500
  if not device_id:
    return "missing param: device_id", 500

  if _MOCK_ENABLED:
    data_records = _get_power_bands_mock_data()
  else:
    data_records = dao.get_power_band_data(device_name, device_id, start)

  return json.dumps(data_records)



def _get_mock_data(device_name, metric):

  metric_to_num_channels = map_metric_name_to_num_channels(device_name)
  num_channels = metric_to_num_channels[metric]

  now = int(time.time() * 1000000 - 5) # micro seconds

  data_records = []
  for i in xrange(5):
    record = {'timestamp': now + i}
    for j in xrange(num_channels):
      channel_name = 'channel_%s' %j
      record[channel_name] = random.random() * 10
    data_records.append(record)

  return data_records


def _get_power_bands_mock_data():

  now = int(time.time() * 1000000 - 5) # micro seconds

  data_records = []
  for i in xrange(5):
    record = {'timestamp': now + i,
              "alpha": random.random() * 10,
              "beta": random.random() * 10,
              "gamma": random.random() * 10,
              "theta": random.random() * 10,
              "delta": random.random() * 10}
    data_records.append(record)

  return data_records


@app.route('/device_names', methods=['GET'])
@support_jsonp
def get_device_names():
  """
  Returns the device names from the metadata file
  :return:
  """
  return json.dumps(get_supported_devices())


@app.route('/registered_devices', methods=['GET'])
@support_jsonp
def get_registered_devices():
  """
  Get the registered devices IDs
  :return:
  """
  if _MOCK_ENABLED:
    registered_devices = ['octopicorn'] # mock ID
  else:
    registered_devices = dao.get_registered_devices()
  return json.dumps(registered_devices)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=WEBSERVER_PORT)
