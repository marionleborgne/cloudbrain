import time

from cloudbrain.connectors.ConnectorInterface import Connector
from cloudbrain.connectors.openbci.OpenBCIBoard import OpenBCIBoard
from cloudbrain.utils.metadata_info import get_num_channels


class OpenBCIConnector(Connector):


  def __init__(self, publishers, buffer_size, step_size, device_type='openbci', device_port='/dev/tty.OpenBCI-DN0094CZ', device_mac=None):
    """

    :return:
    """
    super(OpenBCIConnector, self).__init__(publishers, buffer_size, step_size, device_type, device_port, device_mac)



  def connect_device(self):
    """

    :return:
    """

    self.device = OpenBCIBoard(port=self.device_port)

  def start(self):

    # callback functions to handle the sample for that metric (each metric has a specific number of channels)
    cb_functions = {metric: self.callback_factory(metric, get_num_channels(self.device_name, metric))
                    for metric in self.metrics}

    self.device.start(cb_functions)


  def callback_factory(self, metric_name, num_channels):
    """
    Callback function generator for OpenBCI metrics
    :return: callback function
    """
    def callback(sample):
      """
      Handle OpenBCI samples for that metric
      :param sample: the sample to handle
      """
      message = {}
      for i in range(8):
          channel_value = "%.4f" %(sample.channel_data[i]*10**9) # Nano volts
          message["channel_%s" % i] = channel_value
          message['timestamp'] = int(time.time() * 1000000) # micro seconds

      self.buffers[metric_name].write(message)

    return callback

