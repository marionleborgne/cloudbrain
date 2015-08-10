from connector import Connector
from cloudbrain.connectors.muse.muse_server import MuseServer
import time
import sys
import json


class _unable_to_start_museIO(Exception):
  pass


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

    # Start museIO
    try:
      pass # read: http://stackoverflow.com/questions/89228/calling-an-external-command-in-python
      # TODO: run the command muse-io --osc osc.udp://localhost:9090
    except Exception:
      # TODO: replace Exception by better exception
      raise _unable_to_start_museIO(
        "Unable to start MuseIO. Make sure it is installed or not already running.\n "
        "Read the Muse docs: https://sites.google.com/a/interaxon.ca/muse-developer-site/museio"
      )

    callback_functions = {'eeg': self._eeg_callback,
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


