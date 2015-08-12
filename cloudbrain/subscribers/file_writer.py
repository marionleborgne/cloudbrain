from cloudbrain.subscribers.pika_subscriber import PikaSubscriber
from cloudbrain.utils.metadata_info import map_device_name_to_num_channels, get_supported_metrics, get_supported_devices
import csv
import json
import os
import argparse


_SUPPORTED_DEVICES = get_supported_devices()
_SUPPORTED_METRICS = get_supported_metrics()


class FileWriter(object):
  """
  Subscribes and writes data to a file
  """

  def __init__(self, device_name, device_id, host, metric):
    self.subscriber = PikaSubscriber(device_name=device_name,
                                     device_id=device_id,
                                     host=host,
                                     metric_name=metric)
    self.metric = metric
    self.device_name = device_name
    self.device_id = device_id

    self.csv_writer = None
    self.file = None
    self.headers = None


  def get_headers(self):
    """
    Generate the CSV headers for that metric.
    :return: CSV headers
    """

    metric_to_num_channels = map_device_name_to_num_channels(self.device_name)
    num_channels = metric_to_num_channels[self.metric]
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
      self.csv_writer.writerow([record[column_name] for column_name in self.headers])


def parse_args():
  parser = argparse.ArgumentParser()

  parser.add_argument('-i', '--device_id', required=True,
                      help="A unique ID to identify the device you are sending data from. "
                           "For example: 'octopicorn2015'")
  parser.add_argument('-n', '--device_name', required=True,
                      help="The name of the device your are sending data from. "
                           "Supported devices are: %s" % _SUPPORTED_DEVICES)
  parser.add_argument('-c', '--cloudbrain', default='cloudbrain.rocks',
                      help="The address of the CloudBrain instance you are sending data to.\n"
                           "Use 'cloudbrain.rocks' to send data to our hosted service. \n"
                           "Otherwise use 'localhost' if running CloudBrain locally")
  parser.add_argument('-m', '--metric_name', required=True,
                      help="Name of the metric for which you want to record data.\n"
                           "Supported metrics are %s" % _SUPPORTED_METRICS)

  opts = parser.parse_args()
  if opts.device_name == "openbci" and opts.device_port not in opts:
    parser.error("You have to specify a port for the OpenBCI device!")
  return opts


def main():
  opts = parse_args()

  device_name = opts.device_name
  device_id = opts.device_id
  cloudbrain_address = opts.cloudbrain
  metric_name = opts.metric_name

  run(device_name,
      device_id,
      cloudbrain_address,
      metric_name)


def run(device_name='muse',
        device_id='marion',
        cloudbrain_address='cloudbrain.rocks',
        metric_name='mellow'):
  print "Collecting data ... Ctl-C to stop."
  file_writer = FileWriter(device_name=device_name,
                           device_id=device_id,
                           host=cloudbrain_address,
                           metric=metric_name)
  file_writer.start()


if __name__ == "__main__":
  main()


