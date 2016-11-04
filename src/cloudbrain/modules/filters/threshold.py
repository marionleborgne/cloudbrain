import json
import logging

from cloudbrain.modules.interface import ModuleInterface

_LOGGER = logging.getLogger(__name__)



class ThresholdFilter(ModuleInterface):
    def __init__(self, subscribers, publishers, threshold_values):

        super(ThresholdFilter, self).__init__(subscribers, publishers)
        _LOGGER.debug("Subscribers: %s" % self.subscribers)
        _LOGGER.debug("Publishers: %s" % self.publishers)

        self.threshold_values = threshold_values


    def start(self):
        for subscriber in self.subscribers:
            for metric_buffer in subscriber.metric_buffers.values():
                metric_name = metric_buffer.name
                num_channels = metric_buffer.num_channels
                callback = self._callback_factory(num_channels)
                subscriber.subscribe(metric_name, callback)


    def _callback_factory(self, num_channels):

        publishers = self.publishers


        def callback(unused_ch, unused_method, unused_properties, body):

            for data in json.loads(body):
                data_to_send = {'timestamp': data['timestamp']}
                for i in range(num_channels):
                    channel_name = 'channel_%s' % i
                    if data[channel_name] >= self.threshold_values[i]:
                        data_to_send[channel_name] = 1.0
                    else:
                        data_to_send[channel_name] = 0.0

                for publisher in publishers:
                    for pub_metric_buffer in publisher.metric_buffers.values():
                        pub_metric_name = pub_metric_buffer.name
                        publisher.publish(pub_metric_name, data_to_send)


        return callback
