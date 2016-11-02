import logging
import time

from cloudbrain.connectors.muse_py3 import MuseConnector
from cloudbrain.modules.interface import ModuleInterface

_LOGGER = logging.getLogger(__name__)
_LOGGER.level = logging.DEBUG
_LOGGER.addHandler(logging.StreamHandler())



class MuseSource(ModuleInterface):
    def __init__(self, subscribers, publishers, ip, port, start_muse_io):

        super(MuseSource, self).__init__(subscribers, publishers)
        self.ip = ip
        self.port = port
        self.start_muse_io = start_muse_io

        _LOGGER.debug("Subscribers: %s" % self.subscribers)
        _LOGGER.debug("Publishers: %s" % self.publishers)


    def start(self):

        # Callback functions to handle the sample for that metric.
        # Each metric has a specific number of channels.
        callback_functions = {}

        for publisher in self.publishers:
            for routing_key, metric_buffer in publisher.metric_buffers.items():
                # Note: routing_key is "user_key:metric_name" here.
                if routing_key not in callback_functions:
                    callback_functions[routing_key] = self.callback_factory(
                        metric_buffer.name, metric_buffer.num_channels,
                        publisher)

        connector = MuseConnector(ip=self.ip,
                                  port=self.port,
                                  start_muse_io=self.start_muse_io,
                                  callback_functions=callback_functions)

        _LOGGER.info('Starting muse connector ...')
        connector.start()


    def callback_factory(self, metric_name, num_channels, publisher):
        """
        Callback function generator
        :return: callback function
        """


        def callback(*data):
            """
            Handle muse samples for this metric
            """
            data = data[1:] # the first element is the OSC path
            message = {'timestamp': int(time.time() * 1000000)}  # microseconds
            for i in range(num_channels):
                message["channel_%s" % i] = data[i]
            publisher.publish(metric_name, message)


        return callback
