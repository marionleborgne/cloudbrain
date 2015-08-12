from abc import ABCMeta, abstractmethod

class Publisher(object):
  
  __metaclass__ = ABCMeta
  
  def __init__(self, device_name, device_id, host):
    self.device_name = device_name
    self.device_id = device_id
    self.host = host
  
    
    
  @abstractmethod
  def publish(self, buffer_content):
    """
    Abstract method
    """

  @abstractmethod
  def connect(self):
    """
    Abstract method
    """
    
  @abstractmethod
  def disconnect(self):
    """
    Abstract method
    """

