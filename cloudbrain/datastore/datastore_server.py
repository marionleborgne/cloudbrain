import json
import time
import random
from flask import Flask, request, current_app
from functools import wraps
from cloudbrain.utils.metadata_info import map_device_name_to_num_channels


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True


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
  device_id = request.args.get('device_id', None)
  device_name = request.args.get('device_name', None)
  metric = request.args.get('metric', None)
  start = int(request.args.get('start', (time.time() -5)*1000)) # in ms. return last 5s if start not specified.

  if not device_name:
    return "missing param: device_name", 500
  if not metric:
    return "missing param: metric", 500
  if not device_id:
    return "missing param: device_id", 500

  now = int(time.time() * 1000)

  metric_to_num_channels = map_device_name_to_num_channels(device_name)
  num_channels = metric_to_num_channels[metric]

  data = []
  for i in xrange(now - start):
    record = {'timestamp': start + i}
    for i in xrange(num_channels):
      channel_name = 'channel_%s' %i
      record[channel_name] = random.random() * 10
    data.append(record)

  return json.dumps(data)


if __name__ == '__main__':
  app.run(port=5050)
