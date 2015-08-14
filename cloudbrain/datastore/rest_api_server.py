import time
import json
import random
from flask import Flask, request, current_app
from functools import wraps
from cloudbrain.utils.metadata_info import map_metric_name_to_num_channels, get_supported_devices
from cloudbrain.datastore.CassandraDAL import CassandraDAL
from cloudbrain.settings import WEBSERVER_PORT

_MOCK_ENABLED = None

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
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
  GET the data for a specific device_name
  :return:
  """

  default_start_timestamp = int(time.time() - 5)# return last 5s if start not specified.
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
    data_records = _get_mock_data(device_name, metric, start)
  else:
    data_records = dao.get_data(device_name, device_id, metric, start)

  return json.dumps(data_records)

def _get_mock_data(device_name, metric, start):

  metric_to_num_channels = map_metric_name_to_num_channels(device_name)
  num_channels = metric_to_num_channels[metric]

  now = int(time.time())

  data_records = []
  for i in xrange(now - start):
    record = {'timestamp': start + i}
    for j in xrange(num_channels):
      channel_name = 'channel_%s' %j
      record[channel_name] = random.random() * 10
    data_records.append(record)

  return data_records

@app.route('/devices', methods=['GET'])
@support_jsonp
def get_available_devices():
  return json.dumps(get_supported_devices())


if __name__ == "__main__":
  _MOCK_ENABLED = True
  app.run(host="0.0.0.0", port=WEBSERVER_PORT)
