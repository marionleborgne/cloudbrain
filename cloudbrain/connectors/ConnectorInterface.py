from abc import ABCMeta, abstractmethod

from cloudbrain.utils.metadata_info import get_metrics_names
from cloudbrain.connectors.ConnectorBuffer import ConnectorBuffer


class Connector(object):
  
    __metaclass__ = ABCMeta
  
    def __init__(self, publishers, buffer_size, step_size, device_name, device_port, device_mac=None):

      self.metrics = get_metrics_names(device_name)
      self.device = None
      self.device_port = device_port
      self.device_name = device_name
      self.device_mac = device_mac

      self.buffers = {metric: ConnectorBuffer(buffer_size, step_size, publishers[metric].publish) for metric in self.metrics}
      self.publishers = publishers

      
    @abstractmethod
    def connect_device(self):
      """
      
      :return:
      """
    

      
