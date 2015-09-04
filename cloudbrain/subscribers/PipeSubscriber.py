import json
import sys
from cloudbrain.subscribers.SubscriberInterface import Subscriber
from cloudbrain.utils.metadata_info import get_metrics_names


class PipeSubscriber(Subscriber):
  
  def __init__(self, device_name, device_id, metric_name, pipe_name=None):
    super(PipeSubscriber, self).__init__(device_name, device_id, None)
    self.metric_name = metric_name
    self.pipe_name = pipe_name
    
    
  def connect(self):
    if self.pipe_name is None:
      self.pipe = sys.stdin
    else:
      self.pipe = open(self.pipe_name, 'r')

  def disconnect(self):
    self.connection.close_file()
    
    
  def consume_messages(self, callback):
    while True:
      line = self.pipe.readline()
      if line == '':
        return # EOF

      ## TODO: figure out what ch, method, and properties are
      data = json.loads(line)
      body = data['body']
      callback(None, None, None, json.dumps(body))
    
  def get_one_message(self):
    line = self.pipe.readline()
    return json.loads(line)
    
def _print_message(ch, method, properties, body):
  print body

    
if __name__ == "__main__":

  device_id = "test"
  device_name = "muse"
  host = RABBITMQ_ADDRESS
  buffer_size = 100

  metric_names = get_metrics_names(device_name)

  while 1:
    for metric in metric_names:
      print metric
      subscriber = PikaSubscriber(device_name, device_id, host, metric)
      subscriber.connect()
      #subscriber.consume_messages(_print_message)
      buffer = json.loads(subscriber.get_one_message())
      for record in buffer:
        print record




