#!/usr/bin/python2.7
from cloudbrain.connectors.pika_publisher import PikaPublisher as Publisher
from cloudbrain.settings import DEVICE_METADATA
import argparse
from cloudbrain.utils.metadata_info import get_metrics_names

_SUPPORTED_DEVICES = [device['device_name'] for device in DEVICE_METADATA]


def parse_args():

  parser = argparse.ArgumentParser()

  parser.add_argument('--deviceId', required=True,
                      help="A unique ID to identify the device you are sending data from. For example: 'octopicorn2015'")
  parser.add_argument('--mock', action='store_true', required=False,
                      help="Use this flag to generate mock data for a supported device name %s" % _SUPPORTED_DEVICES)
  parser.add_argument('--deviceName', required=True,
                      help="The name of the device your are sending data from. Supported devices are: %s" %_SUPPORTED_DEVICES)
  parser.add_argument('--cloudbrain', default='cloudbrain.rocks',
                      help="The address of the CloudBrain instance you are sending data to.\n"
                           "Use 'cloudbrain.rocks' to send data to our hosted service. \n"
                           "Otherwise use 'localhost' if running CloudBrain locally")
  parser.add_argument('--bufferSize', default=10,
                      help='Size of the buffer ')
  parser.add_argument('--devicePort', help="Port used for OpenBCI Device.")
  opts = parser.parse_args()
  if opts.deviceName == "openbci" and opts.devicePort not in opts:
    parser.error("You have to specify a port for the OpenBCI device!")
  return opts


def main():

  opts = parse_args()
  mock_data_enabled = opts.mock
  device_name = opts.deviceName
  device_id = opts.deviceId
  cloudbrain_address = opts.cloudbrain
  buffer_size = opts.bufferSize
  device_port = opts.devicePort

  run(device_name,
      mock_data_enabled,
      device_id,
      cloudbrain_address,
      buffer_size,
      device_port)
  

def run(device_name='muse',
         mock_data_enabled=False,
         device_id='test',
         cloudbrain_address='cloudbrain.rocks',
         buffer_size=10,
         device_port='/dev/tty.OpenBCI-DN0094CZ'):

  if device_name == 'muse':
    from cloudbrain.connectors.muse_connector import MuseConnector as Connector
  elif device_name == 'openbci':
    from cloudbrain.connectors.openbci_connector import OpenBCIConnector as Connector
  else:
    raise Exception("Device type '%s' not supported. Supported devices are:%s" %(device_name, _SUPPORTED_DEVICES))

  if mock_data_enabled:
    from cloudbrain.connectors.mock_connector import MockConnector as Connector

  metrics = get_metrics_names(device_name)
  publishers = {metric: Publisher(device_name, device_id, cloudbrain_address, metric) for metric in metrics}
  for publisher in publishers.values():
    publisher.connect()
  if device_name == 'openbci':
    connector = Connector(publishers, buffer_size, device_name, device_port)
  else:
    connector = Connector(publishers, buffer_size, device_name)
  connector.connect_device()
  connector.start()

if __name__ == "__main__":
  #main()
  run()
