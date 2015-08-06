class ConnectorBuffer(object):
  
  def __init__(self, buffer_size, callback):
    self.buffer_size = buffer_size
    self.callback = callback
    self.message_buffer = []
    
  def write(self, datum):
    """
    add one data point to the buffer
    
    :param datum: 
    :return:
    """
    self.message_buffer.append(datum)
    
    if len(self.message_buffer) % self.buffer_size == 0:
      self.callback(self.message_buffer)
      self.message_buffer = []
      
    
    
  
