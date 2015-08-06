from connectors.muse_connector import MuseConnector as Connector
from connectors.pika_publisher import PikaPublisher as Publisher

_DEVICE_ID = "my_device"
_DEVICE_NAME = "openbci"
_HOST = "localhost"
_BUFFER_SIZE = 10

if __name__ == "__main__":
  
  publisher = Publisher(_DEVICE_NAME, _DEVICE_ID, _HOST)
  publisher.connect()
  connector = Connector(publisher, _BUFFER_SIZE, _DEVICE_NAME)
  connector.connectDevice()
  connector.start()
