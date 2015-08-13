from cloudbrain.subscribers.PikaSubscriber import PikaSubscriber
from cloudbrain.utils.metadata_info import get_num_channels, get_supported_metrics, get_supported_devices
from cloudbrain.datastore.CassandraDAL import CassandraDAL
import json
import argparse
from cloudbrain.settings import MOCK_DEVICE_ID, RABBITMQ_ADDRESS

_SUPPORTED_DEVICES = get_supported_devices()
_SUPPORTED_METRICS = get_supported_metrics()


class CassandraSubscriber(object):
  """
  Subscribes and writes data to a file
  """

  def __init__(self, device_name, device_id, rabbitmq_address, metric):
    self.subscriber = PikaSubscriber(device_name=device_name,
                                     device_id=device_id,
                                     rabbitmq_address=rabbitmq_address,
                                     metric_name=metric)
    self.metric = metric
    self.device_name = device_name
    self.device_id = device_id
    self.num_channels = get_num_channels(device_name, metric)

    self.cassandra_dao = CassandraDAL()


  def start(self):
    """
    Consume and write data to file
    :return:
    """

    self.cassandra_dao.connect()
    self.subscriber.connect()
    self.subscriber.consume_messages(self.write_to_cassandra)


  def stop(self):
    """
    Unsubscribe and close file
    :return:
    """
    self.subscriber.disconnect()
    self.file.close_file(self.write_to_cassandra)


  def write_to_cassandra(self, ch, method, properties, body):
    buffer_content = json.loads(body)
    for record in buffer_content:
      timestamp = record["timestamp"]
      channel_data = [record["channel_%s" % i] for i in xrange(self.num_channels)]

      self.cassandra_dao.store_data(timestamp, self.device_id, self.device_name, self.metric, channel_data)


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
        device_id=MOCK_DEVICE_ID,
        cloudbrain_address=RABBITMQ_ADDRESS,
        metric_name='eeg'):
  print "Storing data to Cassandra ... Ctl-C to stop."

  # TODO: need to differentiate between cassandra address and rabbitMQ address. right now cassandra is localhost only
  cassandra_subscriber = CassandraSubscriber(device_name=device_name,
                                             device_id=device_id,
                                             rabbitmq_address=cloudbrain_address,
                                             metric=metric_name)
  cassandra_subscriber.start()


if __name__ == "__main__":
  main()
