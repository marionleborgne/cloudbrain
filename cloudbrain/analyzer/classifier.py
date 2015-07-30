# TODO: see metric_store.py
# 1. subscribe to rabbitMQ 
# 2. load trained model
# 3. run data through trained model

#!/usr/bin/env python
from cloudbrain.listeners.pika_subscriber import PikaSubscriber 
from abc import ABCMeta, abstractmethod

class Classifier(object):
  __metaclass__ = ABCMeta
  
  def __init__(self, device_name, device_id, host):
    self.device_name = device_name
    self.device_id = device_id
    self.host = host
    self.subscriber = PikaSubscriber(self.device_name, self.device_id, self.host)
    
  def initialize(self):  
    self.load_model()
    self.subscriber.connect()
  
  def start(self):
    self.subscriber.consume_messages(self._classify)
    
    
  @abstractmethod
  def _classify(self):
    """
    
    :return:
    """
    
  @abstractmethod
  def load_model(self):
    """
    
    :return:
    """
    
  @abstractmethod 
  def train_model(self):
    """
    
    :return:
    """
    
    
  @abstractmethod
  def save_model(self):
    """
    
    :return:
    """
    
    
