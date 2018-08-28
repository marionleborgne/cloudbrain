import logging

from abc import ABCMeta, abstractmethod

from cloudbrain.core.model import MetricBuffer

_LOGGER = logging.getLogger(__name__)



class SubscriberInterface(object):
    __metaclass__ = ABCMeta


    def __init__(self, base_routing_key):

        self.base_routing_key = base_routing_key
        self.routing_keys = []
        self.metric_buffers = {}


    @abstractmethod
    def connect(self):
        """
        Abstract method
        """
        raise NotImplementedError()


    @abstractmethod
    def register(self, metric_name, num_channels, buffer_size=1):
        raise NotImplementedError()


    @abstractmethod
    def disconnect(self):
        """
        Abstract method
        """
        raise NotImplementedError()


    @abstractmethod
    def subscribe(self, metric_name, callback):
        """
        Abstract method
        """
        raise NotImplementedError()


    @abstractmethod
    def get_one_message(self, metric_name):
        pass


    def metrics_to_num_channels(self):
        metrics_to_num_channels = {}
        for metric_buffer in self.metric_buffers.values():
            num_channels = metric_buffer.num_channels
            metrics_to_num_channels[metric_buffer.name] = num_channels

        return metrics_to_num_channels


    def register_metric(self,
                        routing_key,
                        metric_name,
                        num_channels,
                        buffer_size):

        if routing_key in self.routing_keys:
            _LOGGER.error("Routing key %s already registered. "
                          "Routing keys: %s" % (routing_key,
                                                self.routing_keys))
        else:
            self.routing_keys.append(routing_key)
            self.metric_buffers[routing_key] = MetricBuffer(metric_name,
                                                            num_channels,
                                                            buffer_size)
            _LOGGER.info("New routing key registered: %s" % routing_key)
