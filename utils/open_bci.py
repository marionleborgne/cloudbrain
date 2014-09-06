"""

Core OpenBCI object for handling connections and samples from the board.

EXAMPLE USE:

def handle_sample(sample):
  print(sample.channels)

board = OpenBCIBoard()
board.print_register_settings()
board.start(handle_sample)


"""


import serial
import struct
import numpy as np

SAMPLE_RATE = 250.0  # Hz
START_BYTE = bytes(0xA0)  # start of data packet
END_BYTE = bytes(0xC0)  # end of data packet


def find_port():
    import platform, glob

    s = platform.system()
    if s == 'Linux':
        p = glob.glob('/dev/ttyACM*')

    elif s == 'Darwin':
        p = glob.glob('/dev/tty.usbmodem*')

    if len(p) >= 1:
        return p[0]
    else:
        return None

class OpenBCIBoard(object):
  """

  Handle a connection to an OpenBCI board.

  Args:
    port: The port to connect to.
    baud: The baud of the serial connection.

  """

  def __init__(self, port=None, baud=115200, filter_data=True):
    if not port:
      port = find_port()
      if not port:
        raise OSError('Cannot find OpenBCI port')

    self.ser = serial.Serial(port, baud)
    self.dump_registry_data()
    self.streaming = False
    self.filtering_data = filter_data
    self.channels = 8

  def start(self, callback):
    """

    Start handling streaming data from the board. Call a provided callback
    for every single sample that is processed.

    Args:
      callback: A callback function that will receive a single argument of the
          OpenBCISample object captured.

    """
    if not self.streaming:
      if self.filtering_data:
        self.warn('Enabling filter')
        self.ser.write('f')
        self.ser.readline()

      # Send an 'b' to the board to tell it to start streaming us text.
      self.ser.write('b')
      # Dump the first line that says "Arduino: Starting..."
      self.ser.readline()
      self.streaming = True
    while self.streaming:
      #data = self.ser.readline()
      data = self._read_serial_binary()
      sample = OpenBCISample(data)
      callback(sample)

  """

  Turn streaming off without disconnecting from the board

  """
  def stop(self):
    self.streaming = False

  def disconnect(self):
    self.ser.close()
    self.streaming = False

  """


      SETTINGS AND HELPERS


  """

  def dump_registry_data(self):
    """

    When starting the connection, dump all the debug data until
    we get to a line with something about streaming data.

    """
    line = ''
    while 'begin streaming data' not in line:
      line = self.ser.readline()

  def print_register_settings(self):
    self.ser.write('?')
    for number in xrange(0, 24):
      print(self.ser.readline())

  """

  Adds a filter at 60hz to cancel out ambient electrical noise.

  """
  def enable_filters(self):
    self.ser.write('f')
    self.filtering_data = True;

  def disable_filters(self):
    self.ser.write('g')
    self.filtering_data = False;

  def warn(self, text):
    print(text)

  def _read_serial_binary(self, max_bytes_to_skip=3000):
        """
        Returns (and waits if necessary) for the next binary packet. The
        packet is returned as an array [sample_index, data1, data2, ... datan].

        RAISES
        ------
        RuntimeError : if it has to skip to many bytes.

        serial.SerialTimeoutException : if there isn't enough data to read.
        """
        #global i_sample
        def read(n):
            val = self.ser.read(n)
            # print bytes(val),
            return val

        n_int_32 = self.channels + 1

        # Look for end of packet.
        for i in xrange(max_bytes_to_skip):
            val = read(1)
            if not val:
                if not self.ser.inWaiting():
                    self.warn('Device appears to be stalled. Restarting...')
                    self.ser.write('b\n')  # restart if it's stopped...
                    time.sleep(.100)
                    continue
            # self.ser.write('b\n') , s , x
            # self.ser.inWaiting()
            if bytes(struct.unpack('B', val)[0]) == END_BYTE:
                # Look for the beginning of the packet, which should be next
                val = read(1)
                if bytes(struct.unpack('B', val)[0]) == START_BYTE:
                    if i > 0:
                        self.warn("Had to skip %d bytes before finding stop/start bytes." % i)
                    # Read the number of bytes
                    val = read(1)
                    n_bytes = struct.unpack('B', val)[0]
                    if n_bytes == n_int_32 * 4:
                        # Read the rest of the packet.
                        val = read(4)
                        sample_index = struct.unpack('i', val)[0]
#                         if sample_index != 0:
#                             self.warn("WARNING: sample_index should be zero, but sample_index == %d" % sample_index)
                        # NOTE: using i_sample, a surrogate sample count.
                        t_value = sample_index / float(SAMPLE_RATE)  # sample_index / float(SAMPLE_RATE)
                        #i_sample += 1
                        val = read(4 * (n_int_32 - 1))
                        data = struct.unpack('i' * (n_int_32 - 1), val)
                        data = np.array(data) / (2. ** (24 - 1));  # make so full scale is +/- 1.0
                        # should set missing data to np.NAN here, maybe by testing for zeros..
                        # data[np.logical_not(self.channel_array)] = np.NAN  # set deactivated channels to NAN.
                        data[data == 0] = np.NAN
                        # print data
                        return np.concatenate([[t_value], data])  # A list [sample_index, data1, data2, ... datan]
                    elif n_bytes > 0:
                        print "Warning: Message length is the wrong size! %d should be %d" % (n_bytes, n_int_32 * 4)
                        # Clear the buffer of those bytes.
                        _ = read(n_bytes)
                    else:
                        raise ValueError("Warning: Message length is the wrong size! %d should be %d" % (n_bytes, n_int_32 * 4))
        raise RuntimeError("Maximum number of bytes skipped looking for binary packet (%d)" % max_bytes_to_skip)


  """
  Args:
    channel - An integer from 1-8 incidcating which channel to set.
    toogle_position - An boolean indicating what position the channel should be set to.

  ***NEEDS TO BE TESTED***
  ***TODO: Change cascading ifs to mapping functions

  """
  def set_channel(self, channel, toggle_position):
    #Commands to set toggle to on position
    if toggle_position == 1:
      if channel is 1:
        self.ser.write('q')
      if channel is 2:
        self.ser.write('w')
      if channel is 3:
        self.ser.write('e')
      if channel is 4:
        self.ser.write('r')
      if channel is 5:
        self.ser.write('t')
      if channel is 6:
        self.ser.write('y')
      if channel is 7:
        self.ser.write('u')
      if channel is 8:
        self.ser.write('i')
    #Commands to set toggle to off position
    elif toggle_position == 0:
      if channel is 1:
        self.ser.write('1')
      if channel is 2:
        self.ser.write('2')
      if channel is 3:
        self.ser.write('3')
      if channel is 4:
        self.ser.write('4')
      if channel is 5:
        self.ser.write('5')
      if channel is 6:
        self.ser.write('6')
      if channel is 7:
        self.ser.write('7')
      if channel is 8:
        self.ser.write('8')


class OpenBCISample(object):
  """Object encapulsating a single sample from the OpenBCI board."""

  def __init__(self, data):
    #parts = data.rstrip().split(', ')
    self.id = data[0]
    self.channels = data[1:]
    # for c in xrange(1, len(parts) - 1):
    #   self.channels.append(int(parts[c]))
    # # This is fucking bullshit but I have to strip the comma from the last
    # # sample because the board is returning a comma... wat?
    # self.channels.append(int(parts[len(parts) - 1][:-1]))

