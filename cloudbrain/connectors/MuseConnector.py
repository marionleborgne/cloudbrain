from ConnectorInterface import Connector
from cloudbrain.connectors.muse.MuseOSC import MuseOSC
from cloudbrain.utils.metadata_info import get_num_channels
import time
import sys
import json
import subprocess


class UnableToStartMuseIO(Exception):
    pass


def connect_muse(port=9090):
    """
    Starts muse-io to pair with a muse.
    @param port (int)
        Port used to pair the Muse.

    """
    cmd = ["muse-io", "--osc", "osc.udp://localhost:%s" %port]

    print "\nRunning command: %s" %" ".join(cmd)

    try:
      muse_process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
      muse_process.communicate()
    except OSError:
      raise UnableToStartMuseIO("No able to start muse-io." + \
            "Muse-io is not installed. Go to http://choosemuse.com for more info.")
    except KeyboardInterrupt:
      print "Interrupted !"
      exit(0)

    while True: # look for museIO running keywords
      line = muse_process.stdout.readline()
      if line != '':
        if "OSC messages will be emitted" in line:
          break
      else:
        # muse-io not not running or installed
        raise UnableToStartMuseIO("No able to start muse-io. Go to http://choosemuse.com for more info.")
    print "SUCCESS: MuseIO is running!"


class MuseConnector(Connector):
  def __init__(self, publishers, buffer_size, step_size, device_name='muse', device_port='9090', device_mac=None):
    super(MuseConnector, self).__init__(publishers, buffer_size, step_size, device_name, device_port, device_mac)

  def connect_device(self):

    connect_muse(port=self.device_port)

    # callback functions to handle the sample for that metric (each metric has a specific number of channels)
    cb_functions = {metric: self.callback_factory(metric, get_num_channels(self.device_name, metric))
                    for metric in self.metrics}

    self.device = MuseOSC(self.device_port, cb_functions)

  def start(self):
    try:
      self.device.start()
      while 1:
        time.sleep(1)
    except KeyboardInterrupt:
      sys.exit()


  def callback_factory(self, metric_name, num_args):
    """
    Callback function generator for Muse metrics
    :return: callback function
    """
    def callback(raw_sample):
      """
      Handle muse samples for that metrics
      :param raw_sample: the muse sample to handle
      """
      sample = json.loads(raw_sample)
      data = sample[1]
      message = {"channel_%s" % i: data[i] for i in xrange(num_args)}
      message['timestamp'] = int(time.time() * 1000000) # micro seconds

      self.buffers[metric_name].write(message)

    return callback


