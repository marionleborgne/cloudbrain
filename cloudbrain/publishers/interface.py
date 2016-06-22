import logging

from abc import ABCMeta, abstractmethod

from cloudbrain.core.model import MetricBuffer

_LOGGER = logging.getLogger(__name__)



class PublisherInterface(object):
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
    def publish(self, metric_name, data):
        """
        Abstract method
        """
        raise NotImplementedError()


    def metrics_to_num_channels(self):
        metrics_to_num_channels = {}
        for metric_buffer in self.metric_buffers.values():
            metrics_to_num_channels[metric_buffer.name] = metric_buffer.num_channels

        return metrics_to_num_channels


    def register_metric(self, routing_key, metric_name, num_channels, buffer_size):
        if routing_key in self.routing_keys:
            _LOGGER.error("Routing key %s already registered. "
                          "Routing keys: %s" % (routing_key, self.routing_keys))
        else:
            self.routing_keys.append(routing_key)
            self.metric_buffers[routing_key] = MetricBuffer(metric_name,
                                                            num_channels, buffer_size)
            _LOGGER.info("New routing key registered: %s" % routing_key)
