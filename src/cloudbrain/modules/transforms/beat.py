import time

import json
import logging

from cloudbrain.modules.interface import ModuleInterface

_LOGGER = logging.getLogger(__name__)



class BeatTransformer(ModuleInterface):

    """
    The BPM transformer analyzes only one channel per device and per metric.
    Note that this must be the same channel number across all subscribers.
    This means that you need to subscribe to the same device/metric so that the channel number is
    consistent.
    """
    def __init__(self, subscribers, publishers):

        super(BeatTransformer, self).__init__(subscribers, publishers)
        _LOGGER.debug("Subscribers: %s" % self.subscribers)
        _LOGGER.debug("Publishers: %s" % self.publishers)


    def start(self):
        for subscriber in self.subscribers:
            for metric_buffer in subscriber.metric_buffers.values():
                #metric_name = metric_buffer.name
                #num_channels = metric_buffer.num_channels
                #callback = self._callback_factory(num_channels)
                #subscriber.subscribe(metric_name, callback)
                for publisher in self.publishers:
                    for pub_metric_buffer in publisher.metric_buffers.values():
                        pub_metric_name = pub_metric_buffer.name
                        data_to_send = {'timestamp': None}
                        for i in range(pub_metric_buffer.num_channels):
                            data_to_send['channel_%s' %i] = 1
                        while 1:
                            publisher.publish(pub_metric_name, data_to_send)
                            time.sleep(0.8)


    # def _callback_factory(self, num_channels):
    #
    #     publishers = self.publishers
    #
    #
    #     def process_metric(unused_ch, unused_method, unused_properties, body):
    #
    #         for data in json.loads(body):
    #             data_to_send = {'timestamp': data['timestamp']}
    #             for i in range(num_channels):
    #                 data_to_send['channel_%s' %i] = 1
    #
    #             for i in range(num_channels):
    #                 bpm = data['channel_%s' %i]
    #                 time.sleep(bpm / 60)
    #                 for publisher in publishers:
    #                     for pub_metric_buffer in publisher.metric_buffers.values():
    #                         pub_metric_name = pub_metric_buffer.name
    #                         publisher.publish(pub_metric_name, data_to_send)
    #
    #
    #     return process_metric

