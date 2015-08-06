from connector_buffer import ConnectorBuffer   
from abc import ABCMeta, abstractmethod


class Connector(object):
  
    __metaclass__ = ABCMeta
  
    def __init__(self, publisherInstance, buffer_size, device_name, device_port):
          
      self.device = None
      self.device_port = device_port
      #TODO: we want to have multiple publishers at some point
      self.buffer = ConnectorBuffer(buffer_size, publisherInstance.publish) 
      self.publisherInstance = publisherInstance
      self.device_name = device_name
    
      
    @abstractmethod
    def connectDevice(self):
      """
      
      :return:
      """
    
    #TODO: maybe implement that :-p
    #@abstractmethod
    #def registerPublisher(self):
    #  """
      
    #  :return:
    #  """
      