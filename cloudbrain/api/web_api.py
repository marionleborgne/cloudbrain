__author__ = 'mleborgne'

import json
import time
import datetime
from flask import Flask, request, current_app
from functools import wraps
from cassandra.cluster import Cluster

from settings import SENSOR_ID, METRICS, ANOMALY_LIKELIHOOD_THRESHOLD, DATE_FORMAT

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

# configure cassandra cluster
cluster = Cluster()
session = cluster.connect('sensordata')

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
  GET the data for a specific sensor
  :return:
  """
  sensor = request.args.get('sensor', None)
  metric = request.args.get('metric', None)
  if not sensor or not metric:
    return "", 500
  
  start = int(request.args.get('start', time.time() - 5))
  if len(str(start)) > 10:
    start /= 1000

  # Get data from Cassandra
  start_date = datetime.datetime.fromtimestamp(start).strftime(DATE_FORMAT)  
  column_family_name = "%s_%s" % (sensor, metric)
  cql_select = "SELECT * FROM %s WHERE sensor_id='%s' AND timestamp>'%s';" % (column_family_name, SENSOR_ID, start_date)
  try:
    rows = session.execute(cql_select)
    
  except:
    error = "[ERROR] wrong CQL statement: %s" % cql_select
    return error, 500

  data = []
  for row in rows:
    sensor_id = row[0]
    dt = row[1]  #.strftime(DATE_FORMAT)
    timestamp = int(time.mktime(dt.timetuple()) * 1000)
    anomaly_likelihood = row[2]
    if anomaly_likelihood > ANOMALY_LIKELIHOOD_THRESHOLD:
      anomaly = True
    else:
      anomaly = False
    
    metric_value = row[4]
    prediction = row[5]

    data.append({'sensor_id': sensor_id,
                 'timestamp': timestamp,
                 'anomaly': anomaly,
                 'anomaly_likelihood': anomaly_likelihood,
                 'metric_value': metric_value,
                 'prediction': prediction})
    

  return json.dumps(data)


@app.route('/sensor', methods=['GET'])
@support_jsonp
def sensor():
  """
  GET the last (x,y,z) metric values for this sensor.
  
  JSON returned:
    {
      timestamp: <long>, 
      sensor_id: <string>,
      x: {metric_value: <float>, anomaly_likelihood: <float>, anomaly: <boolean>},
      y: {metric_value: <float>, anomaly_likelihood: <float>, anomaly: <boolean>},
      y: {metric_value: <float>, anomaly_likelihood: <float>, anomaly: <boolean>}
    }

  """
  sensor = request.args.get('name', None)
  # get the data from 5 sec ago to be sure to have at least 1 datapoint
  time_delta_in_s= 5
  start = datetime.datetime.fromtimestamp(int(time.time() - time_delta_in_s)).strftime(DATE_FORMAT)  
  
  result = {'sensor_id': SENSOR_ID}
  last_timestamp = None
  for metric in METRICS:
    column_family_name = "%s_%s" % (sensor, metric)
    cql_select = "SELECT * FROM %s WHERE sensor_id='%s' AND timestamp>'%s';" % (column_family_name, SENSOR_ID, start)
    try:
      rows = session.execute(cql_select)
    except Exception, e:
      error = "[ERROR] wrong CQL statement: %s" % cql_select
      print error
      print e
      return error, 500
    

    if len(rows) == 0:
      return json.dumps([])
    elif len(rows) > 0:
      # get the most recent datapoint
      row = rows[-1]
      current_timestamp = row[1].strftime(DATE_FORMAT)
      if not last_timestamp:
        last_timestamp = current_timestamp
      elif last_timestamp != current_timestamp:
          error = "last timestamp (%s) and current timestamp (%s) are different (current metric: %s)" \
                  % (last_timestamp, current_timestamp, metric)
          return error, 500
      anomaly_likelihood = row[2]
      if anomaly_likelihood > ANOMALY_LIKELIHOOD_THRESHOLD:
        anomaly = True
      else:
        anomaly = False
      
      metric_value = row[4]
      result[metric] = {'metric_value': metric_value,
                        'anomaly_likelihood' : anomaly_likelihood,
                        'anomaly': anomaly}
  result['timestamp'] = last_timestamp    

  return json.dumps(result)


if __name__ == '__main__':
  app.run('0.0.0.0', 5050)
