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


class OpenBCIBoard(object):
  """

  Handle a connection to an OpenBCI board.

  Args:
    port: The port to connect to.
    baud: The baud of the serial connection.

  """

  def __init__(self, port='COM9', baud=115200):
    #self.ser = serial.Serial(port, baud)
    self.dump_registry_data()
    self.streaming = False
    self.filtering_data = False
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
      # Send an 'x' to the board to tell it to start streaming us text.
      self.ser.write('x')
      # Dump the first line that says "Arduino: Starting..."
      self.ser.readline()
      self.streaming = True
    if self.filtering_data:
      print 'Enabling filter'
      self.ser.write('f')
      self.ser.readline()
      self.ser.readline()
    while self.streaming:
      data = self.ser.readline()
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
      #line = self.ser.readline()
      pass

  def print_register_settings(self):
    self.ser.write('?')
    for number in xrange(0, 24):
      print(self.ser.readline())

  """

  Adds a filter at 60hz to cancel out ambient electrical noise.

  """
  def enable_filters(self):
    self.ser.write('f')
    self.filtering_data = True

  def disable_filters(self):
    self.ser.write('g')
    self.filtering_data = False;

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
      if channel is 1:
        self.ser.write('w')
      if channel is 1:
        self.ser.write('e')
      if channel is 1:
        self.ser.write('r')
      if channel is 1:
        self.ser.write('t')
      if channel is 1:
        self.ser.write('y')
      if channel is 1:
        self.ser.write('u')
      if channel is 1:
        self.ser.write('i')
    #Commands to set toggle to off position
    elif toggle_position == 0:
      if channel is 1:
        self.ser.write('1')
      if channel is 1:
        self.ser.write('2')
      if channel is 1:
        self.ser.write('3')
      if channel is 1:
        self.ser.write('4')
      if channel is 1:
        self.ser.write('5')
      if channel is 1:
        self.ser.write('6')
      if channel is 1:
        self.ser.write('7')
      if channel is 1:
        self.ser.write('8')


class OpenBCISample(object):
  """Object encapulsating a single sample from the OpenBCI board."""

  def __init__(self, data):
    parts = data.rstrip().split(', ')
    self.id = parts[0]
    self.channels = []
    for c in xrange(1, len(parts) - 1):
      self.channels.append(int(parts[c]))
    # I have to strip the comma from the last
    # sample because the board is returning a comma... wat?
    self.channels.append(int(parts[len(parts) - 1][:-1]))

