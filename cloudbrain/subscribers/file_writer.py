from cloudbrain.subscribers.pika_subscriber import PikaSubscriber
from cloudbrain.subscribers.dataset_writer import DatasetWriter


class FileWriter(object):

  """
  Subscribes and writes data to a file
  """
  
  def __init__(self, device_name, device_id, host, headers, file_path='training_set.csv'):
    self.subscriber = PikaSubscriber(device_name, device_id, host)
    self.dataset_writer = DatasetWriter(headers, file_path)
    
    
  def start(self):
    """
    Consume and write data to file
    :return:
    """
    self.subscriber.connect()
    self.dataset_writer.open()
    self.subscriber.consume_messages(self.dataset_writer.write)
    
  def stop(self):
    """
    Unsubscribe and close file
    :return:
    """
    self.subscriber.disconnect()
    self.dataset_writer.close()

if __name__ == "__main__":
    
  _DEVICE_ID = "my_device"
  _DEVICE_NAME = "muse"
  _HOST = "localhost"
  _BUFFER_SIZE = 100
  _CSV_HEADERS = ['channel_%s' %i for i in xrange(4)]
  
  headers = ['timestamp'] + _CSV_HEADERS

  print "Collecting data ... Ctl-C to stop :-P" 
  generator = FileWriter(_DEVICE_NAME, _DEVICE_ID, _HOST, headers)
  generator.start()

