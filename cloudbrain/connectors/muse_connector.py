from connector import Connector
from cloudbrain.connectors.muse.muse_server import MuseServer
from cloudbrain.utils.map_metric_names import map_metric_to_num_channels
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
    except OSError:
      raise UnableToStartMuseIO("No able to start muse-io." + \
            "Muse-io is not installed. Go to http://choosemuse.com for more info.")

    while True: # look for museIO running keywords
      line = muse_process.stdout.readline()
      if line != '':
        if "OSC messages will be emitted" in line:
          print "Success: MuseIO is running!"
          break
      else:
        # muse-io not not running or installed
        raise UnableToStartMuseIO("No able to start muse-io. Go to http://choosemuse.com for more info.")




class MuseConnector(Connector):
  def __init__(self, publisher_instance, buffer_size, metric_name, device_name='muse', device_port='9090'):
    super(MuseConnector, self).__init__(publisher_instance, buffer_size, device_name, device_port)
    metric_names_to_num_channels = map_metric_to_num_channels(device_name)
    self.metric_name = metric_name
    self.num_channels = metric_names_to_num_channels[metric_name]

  def connect_device(self):

    connect_muse(port=self.device_port)
    # callback function to handle the sample for that metric (each metric has a specific number of channels)
    callback_function = self.callback_factory(self.num_channels)
    self.device = MuseServer(self.device_port, callback_function)

  def start(self):
    try:
      self.device.start()
      while 1:
        time.sleep(1)
    except KeyboardInterrupt:
      sys.exit()


  '''
  def _eeg_callback(self, raw_sample):
    """
    Callback function handling Muse samples
    :return:
    """
    sample = json.loads(raw_sample)
    data = sample[1]
    message = {"channel_%s" % i: data[i] for i in xrange(4)}
    message['timestamp'] = int(time.time() * 1000000)

    self.buffer.write(message)

  def _hosrseshoe_callback(self, raw_sample):
    """
    Callback function handling Muse samples
    :return:
    """
    sample = json.loads(raw_sample)
    data = sample[1]
    message = {"channel_%s" % i: data[i] for i in xrange(4)}
    message['timestamp'] = int(time.time() * 1000000)

    self.buffer.write(message)

  def _one_arg_callback(self, raw_sample):
    """
    Callback function handling Muse samples
    :return:
    """
    sample = json.loads(raw_sample)
    data = sample[1]
    message = {"channel_0": data[0], 'timestamp': int(time.time() * 1000000)}

    self.buffer.write(message)

  '''

  def _do_nothing(self, sample):
    """
    A dummy callback function that does nothing.
    :param sample: the Muse OSC sample to handle
    """
    pass

  def callback_factory(self, num_args):
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
      message['timestamp'] = int(time.time() * 1000000)

      self.buffer.write(message)

    return callback


