import time
import random

from cloudbrain.connectors.ConnectorInterface import Connector
from cloudbrain.utils.metadata_info import get_num_channels


class MockConnector(Connector):
  
  
  def __init__(self, publishers, buffer_size, step_size, device_name, 
               device_port='mock_port', device_mac=None):
    """
    
    :return:
    """
    super(MockConnector, self).__init__(publishers, buffer_size, step_size,
                                        device_name, device_port, device_mac)
    self.data_generators = [self.data_generator_factory(metric, get_num_channels(self.device_name, metric)) for metric in self.metrics]
    
    
  def connect_device(self):
    """
    Mock connector so actually, don't do anything there :-)  
    :return:
    """
    pass
  
    
  def start(self):

    while 1:
      for data_generator in self.data_generators:
        data_generator()
      time.sleep(0.0001)


  def data_generator_factory(self, metric_name, num_channels):

    def data_generator():

      message = {"channel_%s" % i: 1000 + random.random() * 1000 for i in xrange(num_channels)}
      message['timestamp'] = int(time.time() * 1000000) # micro seconds

      self.buffers[metric_name].write(message)

    return data_generator
    

      
      
