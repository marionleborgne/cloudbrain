from connector import Connector
from cloudbrain.connectors.muse.muse_server import MuseServer
import time
import sys

"""
To start MuseIO, open a terminal or command prompt and type:

muse-io --osc osc.udp://localhost:9090
"""

class MuseConnector(Connector):
  
  
  def __init__(self, publisherInstance, buffer_size, device_port='9090'):
    """
    
    :return:
    """
    super(MuseConnector, self).__init__(publisherInstance, buffer_size, 'muse', device_port)



  def connectDevice(self):
    """
    
    :return:
    """
    
    callback_functions = { 'eeg' : self._eeg_callback}

    
    self.device = MuseServer(self.device_port, callback_functions)
    
  def start(self):
     try:
      self.device.start()
      while 1:
        time.sleep(1)
     except KeyboardInterrupt:
        sys.exit()
    
    
  def _eeg_callback(self, sample):
    """
    Callback function handling Muse samples
    :return:
    """
    
    message = {"channel_%s" % i: sample[i] for i in xrange(4)}
    message['timestamp'] = int(time.time() * 1000)
    
    self.buffer.write(message)
      
      



