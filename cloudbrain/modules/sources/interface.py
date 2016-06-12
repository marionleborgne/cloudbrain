from abc import ABCMeta, abstractmethod



class SourceInterface(object):
  """
  A source has only outputs. No inputs.
  """

  __metaclass__ = ABCMeta


  def __init__(self, subscribers, publishers):
    """
    
    :param source_type: (string) type of the device processed by this module 
    :return: 
    """
    
    if len(subscribers) > 0:
      raise ValueError("A source can only have publishers")
    
    assert isinstance(publishers, list)
    assert isinstance(subscribers, list)
    
    self.publishers = publishers
    self.subscribers = subscribers
    

  @abstractmethod
  def start(self):
    raise NotImplementedError()
