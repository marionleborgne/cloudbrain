import logging

from cloudbrain.connectors.neurosky import NeuroskyConnector
from cloudbrain.connectors.thinkgear import THINKGEAR_DEVICE_SERIAL_PORT
from cloudbrain.modules.interface import ModuleInterface

_LOGGER = logging.getLogger(__name__)
_LOGGER.level = logging.DEBUG
_LOGGER.addHandler(logging.StreamHandler())


class NeuroskySource(ModuleInterface):
    def __init__(self, subscribers, publishers,
                 device_address=THINKGEAR_DEVICE_SERIAL_PORT, verbosity=0):

        super(NeuroskySource, self).__init__(subscribers, publishers)
        self.device_address = device_address
        self.verbosity = verbosity

        _LOGGER.debug("Subscribers: %s" % self.subscribers)
        _LOGGER.debug("Publishers: %s" % self.publishers)

    def start(self):

        # Callback functions to handle the sample for that metric.
        # Each metric has a specific number of channels.
        callback_functions = {}

        for publisher in self.publishers:
            for routing_key, metric_buffer in publisher.metric_buffers.items():
                metric_name = metric_buffer.name
                if metric_name not in callback_functions:
                    callback_functions[metric_name] = self.callback_factory(
                        metric_name, publisher)

        connector = NeuroskyConnector(callback_functions=callback_functions,
                                      device_address=self.device_address,
                                      verbosity=self.verbosity)

        _LOGGER.info('Starting connector ...')
        connector.start()

    @staticmethod
    def callback_factory(metric_name, publisher):
        """
        Callback function generator
        :return: callback function
        """

        def callback(timestamp, sample):
            """Handle metric sample."""
            message = {'timestamp': timestamp, 'channel_0': sample}
            publisher.publish(metric_name, message)

        return callback
