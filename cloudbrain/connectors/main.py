#!/usr/bin/python2.7
from cloudbrain.connectors.pika_publisher import PikaPublisher as Publisher
from cloudbrain.settings import DEVICE_METADATA
import argparse

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

  if device_name == 'muse':
    from cloudbrain.connectors.muse_connector import MuseConnector as Connector
  elif device_name == 'openbci':
    from cloudbrain.connectors.openbci_connector import OpenBCIConnector as Connector
  else:
    raise Exception("Device type '%s' not supported. Supported devices are:%s" %(device_name, _SUPPORTED_DEVICES))

  if mock_data_enabled:
    from cloudbrain.connectors.mock_connector import MockConnector as Connector

  publisher = Publisher(device_name, device_id, cloudbrain_address)
  publisher.connect()
  if device_name == 'openbci':
    connector = Connector(publisher, buffer_size, device_name, device_port)
  else:
    connector = Connector(publisher, buffer_size, device_name)
  connector.connectDevice()
  connector.start()



if __name__ == "__main__":
  main()
