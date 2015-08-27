import json
import sys, os
import os.path
import stat

from cloudbrain.publishers.PublisherInterface import Publisher

from threading import Lock


class PipePublisher(Publisher):
  """
  Publisher implementation for writing data to pipe
  """
  PIPE_WRITING_LOCKS = dict()

  def __init__(self, device_name, device_id, metric_name, pipe_name=None):
    super(PipePublisher, self).__init__(device_name, device_id, None)
    self.metric_name = metric_name
    self.pipe_name = pipe_name
    

  def get_lock(self):
    lock = PipePublisher.PIPE_WRITING_LOCKS.get(self.pipe_name, None)
    if lock is None:
      lock = Lock()
      PipePublisher.PIPE_WRITING_LOCKS[self.pipe_name] = lock
    return lock
    
  def lock(self):
    lock = self.get_lock()
    lock.acquire(True)

  def unlock(self):
    lock = self.get_lock()
    lock.release()
    
  def publish(self, buffer_content):
    key = "%s:%s:%s" % (self.device_id, self.device_name, self.metric_name)
    out = {"key": key, 'body': buffer_content}
    to_write = json.dumps(out)

    self.lock()

    self.pipe.write(to_write)
    self.pipe.write("\n")
    self.pipe.flush()

    self.unlock()

  def connect(self):
    self.lock()
    
    if self.pipe_name is None:
      self.pipe = sys.stdout
    else:
      if os.path.exists(self.pipe_name) and not stat.S_ISFIFO(os.stat(self.pipe_name).st_mode):
        raise Exception("File '%s' exists and is not a named pipe." % self.pipe_name)
      elif not os.path.exists(self.pipe_name):
        os.mkfifo(self.pipe_name)
      self.pipe = open(self.pipe_name, 'a')

    self.unlock()
    
  def disconnect(self):
    if self.pipe_name is not None:
      self.pipe.close()
      os.remove(self.pipe_name)

