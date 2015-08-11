from connector_buffer import ConnectorBuffer   
from abc import ABCMeta, abstractmethod


class Connector(object):
  
    __metaclass__ = ABCMeta
  
    def __init__(self, publisher_instance, buffer_size, device_name, device_port):
          
      self.device = None
      self.device_port = device_port
      self.buffer = ConnectorBuffer(buffer_size, publisher_instance.publish)
      self.publisherInstance = publisher_instance
      self.device_name = device_name
    
      
    @abstractmethod
    def connect_device(self):
      """
      
      :return:
      """
    

      