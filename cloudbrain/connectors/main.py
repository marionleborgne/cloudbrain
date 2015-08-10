from cloudbrain.connectors.pika_publisher import PikaPublisher as Publisher
from cloudbrain.settings import DEVICE_METADATA
import json


_DEVICE_ID = "my_device"
_DEVICE_NAME = "openbci"
_HOST = "localhost"
_BUFFER_SIZE = 10

def parse_args():
 	
  parser = argparse.ArgumentsParser()

  parser.add_argument('--user-id', required=True,
                      help='Make user-id unique to you.')
  parser.add_argument('--device-name', required=True,
                      help="Enter device_name: 'openbci', 'muse', 'sensortag', 'mock'")
  parser.add_argument('--host', default='cloudbrain.rocks',
                      help="To send data to cloudbrain use 'cloudbrain.rocks'. Otherwise use 'localhost' if running locally")
  parser.add_argument('--buffer-size', default=10,
                      help='Change at your own pleasure.')
  opts = parser.parse_args()

  return opts

def main():
	
	device_names = [el['device_name'] for el in DEVICE_METADATA]
	opts = parse_args()
	device_type = opts.device_name
	device_id = opts.user_id
	cloudbrain_addr = opts.host
	buffer_size = opts.buffer_size

	if opts.device_name = 'muse':
		from cloudbrain.connectors.muse_connector import MuseConnector as Connector
	elif opts.device_name = 'openbci':
		from cloudbrain.connectors.openbci_connector import OpenBCIConnector as Connector
	elif opts.device_name = 'mock'
		from cloudbrain.connectors.mock_connector import MockConnector as Connector
	else:
		raise Exception("Device type '%s' not supported."%opts.device_name)

	publisher = Publisher(device_type, device_id, cloudbrain_addr)
  	publisher.connect()
  	connector = Connector(publisher, buffer_size, device_type)
  	connector.connectDevice()
  	connector.start()




if __name__ == "__main__":
  
  main()
