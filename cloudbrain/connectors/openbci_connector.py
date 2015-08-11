from connector import Connector
from cloudbrain.connectors.openbci.openbci_v3 import OpenBCIBoard
import time


class OpenBCIConnector(Connector):


  def __init__(self, publisherInstance, buffer_size, device_type='openbci', device_port='/dev/tty.OpenBCI-DN0094CZ'):
    """

    :return:
    """
    super(OpenBCIConnector, self).__init__(publisherInstance, buffer_size, device_type, device_port)



  def connect_device(self):
    """

    :return:
    """

    self.device = OpenBCIBoard(port=self.device_port)

  def start(self):
    self.device.start(self._handle_sample)


  def _handle_sample(self, sample):
    """
    Callback function handling OpenBCI samples
    :return:
    """

    message = {"channel_%s" % i: sample.channel_data[i] for i in xrange(8)}
    message['timestamp'] = int(time.time() * 1000)

    self.buffer.write(message)





