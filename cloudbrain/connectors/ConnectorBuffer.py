class ConnectorBuffer(object):

  def __init__(self, buffer_size, step_size, callback):
    self.buffer_size = buffer_size
    self.step_size = step_size
    self.callback = callback
    self.message_buffer = []

    self.count = 0

  def write(self, datum):
    """
    add one data point to the buffer

    :param datum:
    :return:
    """
    self.message_buffer.append(datum)
    self.count += 1

    # print(len(self.message_buffer), self.count, self.step_size, self.buffer_size)

    # if len(self.message_buffer) % self.buffer_size == 0:
    if self.count >= self.step_size and len(self.message_buffer) >= self.buffer_size:
      self.callback(self.message_buffer[-self.buffer_size:])
      self.message_buffer = self.message_buffer[-self.buffer_size:]
      self.count = 0
