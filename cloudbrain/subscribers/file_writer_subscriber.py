from cloudbrain.subscribers.PikaSubscriber import PikaSubscriber
from cloudbrain.subscribers.PipeSubscriber import PipeSubscriber
from cloudbrain.utils.metadata_info import get_num_channels, get_supported_metrics, get_supported_devices
from cloudbrain.settings import RABBITMQ_ADDRESS, MOCK_DEVICE_ID
import csv
import json
import os
import argparse


_SUPPORTED_DEVICES = get_supported_devices()
_SUPPORTED_METRICS = get_supported_metrics()


class FileWriterSubscriber(object):
  """
  Subscribes and writes data to a file
  """

  def __init__(self, device_name, device_id,  metric, subscriber_type="pika", rabbitmq_address=None, pipe_name=None):
    if subscriber_type == "pika" and rabbitmq_address is None:
      raise ValueError("Pika subscriber needs to have a rabbitmq address!")

    if subscriber_type == "pika":
      self.subscriber = PikaSubscriber(device_name=device_name,
                                       device_id=device_id,
                                       rabbitmq_address=rabbitmq_address,
                                       metric_name=metric)
    elif subscriber_type == "pipe":
      self.subscriber = PipeSubscriber(device_name=device_name,
                                       device_id=device_id,
                                       metric_name=metric,
                                       pipe_name=pipe_name)
    else:
      raise ValueError("'%s' is not a valid subscriber type. Valid types are %s." % (subscriber_type, "pika, pipe"))
    self.metric = metric
    self.device_name = device_name
    self.device_id = device_id

    self.subscriber_type = subscriber_type

    self.csv_writer = None
    self.file = None
    self.headers = None


  def get_headers(self):
    """
    Generate the CSV headers for that metric.
    :return: CSV headers
    """

    num_channels = get_num_channels(self.device_name,self.metric)
    headers = ['timestamp'] + ['channel_%s' % i for i in xrange(num_channels)]
    return headers


  def init_file(self):
    """
    Open file and write headers.
    :return:
    """
    if not os.path.exists("data"):
      os.mkdir("data")
    file_path = os.path.join("data", "%s_%s_%s.csv" % (self.device_id, self.device_name, self.metric))
    self.file = open(file_path, 'wb')
    self.csv_writer = csv.writer(self.file)
    self.csv_writer.writerow(self.headers)


  def start(self):
    """
    Consume and write data to file
    :return:
    """

    self.headers = self.get_headers()
    self.init_file()
    self.subscriber.connect()
    self.subscriber.consume_messages(self.write)


  def stop(self):
    """
    Unsubscribe and close file
    :return:
    """
    self.subscriber.disconnect()
    self.file.close_file()


  def write(self, ch, method, properties, body):
    buffer_content = json.loads(body)
    for record in buffer_content:
      self.csv_writer.writerow([record.get(column_name, None) for column_name in self.headers])


def parse_args():
  parser = argparse.ArgumentParser()

  parser.add_argument('-i', '--device_id', required=True,
                      help="A unique ID to identify the device you are sending data from. "
                           "For example: 'octopicorn2015'")
  parser.add_argument('-n', '--device_name', required=True,
                      help="The name of the device your are sending data from. "
                           "Supported devices are: %s" % _SUPPORTED_DEVICES)
  parser.add_argument('-c', '--cloudbrain', default=RABBITMQ_ADDRESS,
                      help="The address of the CloudBrain instance you are sending data to.\n"
                           "Use " + RABBITMQ_ADDRESS + " to send data to our hosted service. \n"
                           "Otherwise use 'localhost' if running CloudBrain locally")
  parser.add_argument('-p', '--pipe', default=None,
                      help="The pipe you are sending data to, for pipe subscriber.\n"
                           "The default is to read from standard input.")
  parser.add_argument('-m', '--metric_name', required=True,
                      help="Name of the metric for which you want to record data.\n"
                           "Supported metrics are %s" % _SUPPORTED_METRICS)
  parser.add_argument('-S', '--subscriber', default="pika",
                      help="The subscriber to use to get the data.\n"
                      "Possible options are pika, pipe.\n"
                      "The default is pika.")
  

  opts = parser.parse_args()
  if opts.device_name == "openbci" and opts.device_port is not None:
    parser.error("You have to specify a port for the OpenBCI device!")
  return opts


def main():
  opts = parse_args()

  device_name = opts.device_name
  device_id = opts.device_id
  cloudbrain_address = opts.cloudbrain
  metric_name = opts.metric_name
  pipe_name = opts.pipe
  subscriber_type = opts.subscriber
  
  run(device_name,
      device_id,
      cloudbrain_address,
      metric_name,
      pipe_name,
      subscriber_type)


def run(device_name='muse',
        device_id=MOCK_DEVICE_ID,
        cloudbrain_address=RABBITMQ_ADDRESS,
        metric_name='mellow',
        pipe_name=None,
        subscriber_type='pika'):
  print "Collecting data ... Ctl-C to stop."
  file_writer = FileWriterSubscriber(device_name=device_name,
                           device_id=device_id,
                           rabbitmq_address=cloudbrain_address,
                           metric=metric_name,
                           pipe_name=pipe_name,
                           subscriber_type=subscriber_type)
  file_writer.start()


if __name__ == "__main__":
  main()


