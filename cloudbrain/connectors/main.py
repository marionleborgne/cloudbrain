from muse_connector import MuseConnector as Connector
from pika_publisher import PikaPublisher as Publisher

_DEVICE_ID = "my_device"
_DEVICE_NAME = "muse"
_HOST = "localhost"
_BUFFER_SIZE = 100

if __name__ == "__main__":
  
  publisher = Publisher(_DEVICE_NAME, _DEVICE_ID, _HOST)
  publisher.connect()
  connector = Connector(publisher, _BUFFER_SIZE)
  connector.connectDevice()
  connector.start()
