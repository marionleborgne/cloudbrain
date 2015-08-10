from connector import Connector
from cloudbrain.connectors.muse.muse_server import MuseServer
from cloudbrain.connectors.pika_publisher import PikaPublisher
import time
import sys
import json

"""
To start MuseIO, open a terminal or command prompt and type:

muse-io --osc osc.udp://localhost:9090
"""

class MuseConnector(Connector):
  
  
  def __init__(self, publisherInstance, buffer_size, device_type='muse', device_port='9090'):
    """
    
    :return:
    """
    super(MuseConnector, self).__init__(publisherInstance, buffer_size, device_type, device_port)



  def connectDevice(self):
    """
    
    :return:
    """
    
    callback_functions = { 'eeg' : self._eeg_callback,
                           'concentration': self._do_nothing,
                           'mellow': self._do_nothing,
                           'horseshoe': self._do_nothing}

    
    self.device = MuseServer(self.device_port, callback_functions)
    
  def start(self):
     try:
      self.device.start()
      while 1:
        time.sleep(1)
     except KeyboardInterrupt:
        sys.exit()
    
    
  def _eeg_callback(self, raw_sample):
    """
    Callback function handling Muse samples
    :return:
    """
    sample = json.loads(raw_sample)
    path = sample[0]
    data = sample[1]
    message = {"channel_%s" % i: data[i] for i in xrange(4)}
    message['timestamp'] = int(time.time() * 1000000)
    
    self.buffer.write(message)
    
  def _mellow_callback(self, raw_sample):
    """
    Callback function handling Muse samples
    :return:
    """
    sample = json.loads(raw_sample)
    path = sample[0]
    data = sample[1]
    message = {"mellow": data[0], 'timestamp': int(time.time() * 1000000)}

    self.buffer.write(message)
      
      
  def _do_nothing(self, sample):
    pass

if __name__ == "__main__":

  _DEVICE_ID = "my_device"
  _DEVICE_NAME = "openbci"
  _HOST = "localhost"
  _BUFFER_SIZE = 10

  publisher = PikaPublisher(_DEVICE_NAME, _DEVICE_ID, _HOST)
  publisher.connect()
  connector = MuseConnector(publisher, _BUFFER_SIZE, _DEVICE_NAME)
  connector.connectDevice()
  connector.start()
