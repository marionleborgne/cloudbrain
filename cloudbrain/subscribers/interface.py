from abc import ABCMeta, abstractmethod



class SubscriberInterface(object):
  __metaclass__ = ABCMeta


  def __init__(self, host):
    self.host = host


  @abstractmethod
  def connect(self):
    pass


  @abstractmethod
  def disconnect(self):
    pass


  @abstractmethod
  def register(self, routing_key):
    pass


  @abstractmethod
  def subscribe(self, routing_key, callback):
    pass


  @abstractmethod
  def get_one_message(self, routing_key):
    pass

