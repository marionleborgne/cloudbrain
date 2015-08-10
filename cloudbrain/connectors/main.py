from cloudbrain.connectors.pika_publisher import PikaPublisher as Publisher

from cloudbrain.connectors.muse_connector import MuseConnector as Connector
from cloudbrain.connectors.mock_connector import MockConnector as Connector
from cloudbrain.connectors.openbci_connector import OpenBCIConnector as Connector


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
