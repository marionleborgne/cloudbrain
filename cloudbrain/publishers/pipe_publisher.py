import argparse

from cloudbrain.publishers.PipePublisher import PipePublisher as Publisher
from cloudbrain.utils.metadata_info import get_metrics_names, get_supported_devices
from cloudbrain.settings import RABBITMQ_ADDRESS, MOCK_DEVICE_ID

_SUPPORTED_DEVICES = get_supported_devices()


def parse_args():
  parser = argparse.ArgumentParser()

  parser.add_argument('-i', '--device_id', required=True,
                      help="A unique ID to identify the device you are sending data from. "
                           "For example: 'octopicorn2015'")
  parser.add_argument('-m', '--mock', action='store_true', required=False,
                      help="Use this flag to generate mock data for a "
                           "supported device name %s" % _SUPPORTED_DEVICES)
  parser.add_argument('-n', '--device_name', required=True,
                      help="The name of the device your are sending data from. "
                           "Supported devices are: %s" % _SUPPORTED_DEVICES)
  parser.add_argument('-o', '--output', default=None,
                      help="The named pipe you are sending data to (e.g. /tmp/eeg_pipe).\n"
                           "The publisher will create the pipe.\n"
                           "By default this is the standard output.")
  parser.add_argument('-b', '--buffer_size', default=10,
                      help='Size of the buffer ')
  parser.add_argument('-p', '--device_port', help="Port used for OpenBCI Device.")

  opts = parser.parse_args()
  if opts.device_name == "openbci" and opts.device_port not in opts:
    parser.error("You have to specify a port for the OpenBCI device!")
  return opts


def main():
  opts = parse_args()
  mock_data_enabled = opts.mock
  device_name = opts.device_name
  device_id = opts.device_id
  buffer_size = opts.buffer_size
  device_port = opts.device_port
  pipe_name = opts.output

  run(device_name,
      mock_data_enabled,
      device_id,
      buffer_size,
      device_port,
      pipe_name)


def run(device_name='muse',
        mock_data_enabled=True,
        device_id=MOCK_DEVICE_ID,
        buffer_size=10,
        device_port='/dev/tty.OpenBCI-DN0094CZ',
        pipe_name=None):
  if device_name == 'muse':
    from cloudbrain.connectors.MuseConnector import MuseConnector as Connector
  elif device_name == 'openbci':
    from cloudbrain.connectors.OpenBCIConnector import OpenBCIConnector as Connector
  else:
    raise Exception("Device type '%s' not supported. Supported devices are:%s" % (device_name, _SUPPORTED_DEVICES))

  if mock_data_enabled:
    from cloudbrain.connectors.MockConnector import MockConnector as Connector

  metrics = get_metrics_names(device_name)
  publishers = {metric: Publisher(device_name, device_id, metric, pipe_name) for metric in metrics}
  if pipe_name is not None:
    print("Opening pipe...")
    print("Note that it won't open until you also read from it")

  for publisher in publishers.values():
    publisher.connect()
    
  if pipe_name is not None:
    print("Opened pipe!")
  if device_name == 'openbci':
    connector = Connector(publishers, buffer_size, device_name, device_port)
  else:
    connector = Connector(publishers, buffer_size, device_name)
  connector.connect_device()
  

  connector.start()

if __name__ == "__main__":
  main()
  #run('muse', False, 'marion', RABBITMQ_ADDRESS)
