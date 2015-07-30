from openbci_connector import OpenBCIConnector as Connector
from pika_publisher import PikaPublisher as Publisher

_DEVICE_ID = "mock_device"
_DEVICE_NAME = "openbci"
_HOST = "localhost"
_BUFFER_SIZE = 100

if __name__ == "__main__":
  
  publisher = Publisher(_DEVICE_NAME, _DEVICE_ID, _HOST)
  publisher.connect()
  connector = Connector(publisher, _BUFFER_SIZE)
  connector.connectDevice()
  connector.start()
