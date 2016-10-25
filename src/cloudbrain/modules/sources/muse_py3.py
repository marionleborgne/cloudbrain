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
            metrics_to_num_channels = publisher.metrics_to_num_channels()
            for (metric_name, num_channels) in metrics_to_num_channels.items():
                if metric_name not in callback_functions:
                    callback_functions[metric_name] = self.callback_factory(
                        metric_name, num_channels)

        connector = MuseConnector(ip=self.ip,
                                  port=self.port,
                                  start_muse_io=self.start_muse_io,
                                  callback_functions=callback_functions)

        _LOGGER.info('Starting muse connector ...')
        connector.start()


    def callback_factory(self, metric_name, num_channels):
        """
        Callback function generator
        :return: callback function
        """


        def callback(osc_path, *data):
            """
            Handle muse samples for this metric
            """
            message = {"channel_%s" % i: data[i] for i in range(num_channels)}
            message['timestamp'] = int(time.time() * 1000000)  # micro seconds

            for publisher in self.publishers:
                publisher.publish(metric_name, message)


        return callback
