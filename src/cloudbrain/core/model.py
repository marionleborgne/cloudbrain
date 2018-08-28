"""
Cloudbrain's OO data model.
"""
  

class MetricBuffer(object):
  def __init__(self, name, num_channels, buffer_size):
    self.name = name
    self.num_channels = num_channels
    self.metric_names = ["channel_%s" % i for i in range(self.num_channels)]
    self.metric_names.append("timestamp")

    self.buffer_size = buffer_size
    self.data_buffer = []

  def _validate_datum(self, datum):
    """
    Validate if the datum being sent is following the right schema. 
    
    :param datum: MetricBuffer data point. E.g:
       {"timestamp": <float>, "metric_0": <float>, ..., "metric_7": <float>}
    :type datum: dict
    """
    if sorted(datum.keys()) != sorted(self.metric_names):
        raise ValueError("MetricBuffer keys should be %s but are %s" % (
          self.metric_names, datum.keys()))


  def add(self, datum):
    """
    Append datum to the buffer. 
    
    :param datum: metric data point with the following format:
      {"timestamp": <float>, "metric_0": <float>, ..., "metric_7": <float>}
    :type datum: dict
    
    :returns: (list of dicts) 'None' if the buffer isn't full yet. 
      A list of dicts otherwise. E.g: 
      [
        {"timestamp": <float>, "metric_0": <float>, ..., "metric_7": <float>},
        ...
        {"timestamp": <float>, "metric_0": <float>, ..., "metric_7": <float>}
      ] 
    :rtype: list of dicts
    """
    self._validate_datum(datum)    
    
    self.data_buffer.append(datum)
    if len(self.data_buffer) >= self.buffer_size:
      data_buffer = self.data_buffer
      self.data_buffer = []
      return data_buffer
    else:
      return None
