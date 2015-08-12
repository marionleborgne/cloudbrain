__author__ = 'mleborgne'

from cassandra.cluster import Cluster
import time
import pika
import json
import importlib

"""
Subscribes to rabbitMQ and stores data in cassandra
"""

# configure cassandra cluster
cluster = Cluster()
session = cluster.connect('cloudbrain')

# configure and connect RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(
  host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange=SENSOR,
                         type='fanout')
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange=SENSOR,
                   queue=queue_name)

def getModelParamsFromName(metric_name):
  importName = "model_params.%s" % metric_name
  print "Importing model params from %s" % importName
  try:
    importedModelParams = importlib.import_module(importName).MODEL_PARAMS
  except ImportError:
    raise Exception("No model params exist for '%s'." % metric_name)
  return importedModelParams


def callback(ch, method, properties, body):
  timestamp = int(time.time() * 1000)
  data = json.loads(body)
  store_data(timestamp, metric, metric_value, prediction, anomalyScore, anomalyLikelihood)


def store_data(timestamp, metric, metric_value, prediction, anomalyScore, anomalyLikelihood):
  column_values = "'%s', %s, %s, %s, %s, %s" % (SENSOR_ID, timestamp, metric_value, prediction, anomalyScore, anomalyLikelihood)

  column_family = "%s_%s" % (SENSOR, metric)
  columns = "sensor_id, timestamp, %s" %','.join(COLUMNS)
  cql_insert = "INSERT INTO %s (%s) VALUES (%s);" % (column_family, columns, column_values)
  print cql_insert

  try:
    session.execute(cql_insert)
  except:
    print "DEBUG: CQL insert: %s" % cql_insert
      


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()

print "waiting for data on exchange '%s' ..." % SENSOR