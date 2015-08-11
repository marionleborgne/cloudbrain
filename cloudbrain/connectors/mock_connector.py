from connector import Connector
import time
import random


class MockConnector(Connector):
  
  
  def __init__(self, publisherInstance, buffer_size, device_name, device_port='mock_port'):
    """
    
    :return:
    """
    super(MockConnector, self).__init__(publisherInstance, buffer_size, device_name, device_port)
    self.mock_generators = {'openbci': self._generate_OpenBCI_data,
                       'muse': self._generate_Muse_data}
    
    
  def connect_device(self):
    """
    Mock connector so actually, don't do anything there :-)  
    :return:
    """
    
    pass
  
    
  def start(self):
    
    while 1:
      self._generate_data()
    
   
  def _generate_OpenBCI_data(self):
    message = {"channel_%s" % i: random.random() * 10 for i in xrange(8)}
    message['timestamp'] = int(time.time() * 1000)
    return message
  
  
  def _generate_Muse_data(self):
    message = {"channel_%s" % i: random.random() * 10 for i in xrange(4)}
    message['timestamp'] = int(time.time() * 1000)
    return message
     
    
    
  def _generate_data(self):
    """
    Just generate data
    :return:
    """
  
    self.buffer.write(self.mock_generators[self.device_name]())
      
      
