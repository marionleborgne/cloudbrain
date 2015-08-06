from abc import ABCMeta, abstractmethod

class Subscriber(object):
  __metaclass__ = ABCMeta
  
  def __init__(self,  device_name, device_id, host):
    """
    
    :return:
    """
    self.device_name = device_name
    self.device_id = device_id
    self.host = host

  @abstractmethod
  def consume_messages(self, callback):
    #TODO: write doc
    """
    
    :return:
    """
  @abstractmethod
  def connect(self):
    #TODO: write doc
    """
    
    :return:
    """
    
  @abstractmethod
  def disconnect(self):
    #TODO: write doc
    """
    
    :return:
    """