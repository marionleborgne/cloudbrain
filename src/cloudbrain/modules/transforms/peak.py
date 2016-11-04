import peakutils

import numpy as np

import json
import logging

from cloudbrain.modules.interface import ModuleInterface

_LOGGER = logging.getLogger(__name__)



class PeakTransformer(ModuleInterface):

    """
    The peak transformer analyzes only one channel per device and per metric.
    Note that this must be the same channel number across all subscribers.
    This means that you need to subscribe to the same device/metric so that the
    channel number is consistent.
    """
    def __init__(self, subscribers, publishers, window_size, channel_number):

        super(PeakTransformer, self).__init__(subscribers, publishers)
        _LOGGER.debug("Subscribers: %s" % self.subscribers)
        _LOGGER.debug("Publishers: %s" % self.publishers)

        self.window_size = window_size
        self.channel_number = channel_number
        self.channel_name = 'channel_%s' %channel_number
        self.windows = {}


    def start(self):
        for subscriber in self.subscribers:
            for metric_buffer in subscriber.metric_buffers.values():
                metric_name = metric_buffer.name

                self.windows[metric_name] = {'timestamps': [],
                                             'data_to_analyze': []}

                callback = self._callback_factory(metric_name)
                subscriber.subscribe(metric_buffer.name, callback)


    def _callback_factory(self, metric_name):

        publishers = self.publishers


        def process_metric(unused_ch, unused_method, unused_properties, body):

            peaks = self._find_peaks(json.loads(body), metric_name)

            if peaks:
                for i in range(len(peaks['timestamp'])):
                    data = {}
                    for channel_name, window_data in peaks.items():
                        data[channel_name] = window_data[i]
                    for publisher in publishers:
                        metric_buffers = publisher.metric_buffers
                        for pub_metric_buffer in metric_buffers.values:
                            pub_metric_name = pub_metric_buffer.name
                            publisher.publish(pub_metric_name, data)


        return process_metric


    def _find_peaks(self, cb_buffer, metric_name):
        """

        :param cb_buffer:
        :param metric_name:
        :param num_channels:
        :return: peaks
        {
            'timestamps': [1, 2, ..., 100]
            'channel_0': [3.2, 0.1, ..., 23.0]
                ...
            'channel_7': [3.2, 0.1, ..., 23.0]
        }
        """

        peaks = None
        for data in cb_buffer:

            value = data[self.channel_name]
            self.windows[metric_name]['data_to_analyze'].append(value)
            self.windows[metric_name]['timestamps'].append(data['timestamp'])
            if len(self.windows[metric_name]['timestamps']) == self.window_size:
                compute_peaks = True
            else:
                compute_peaks = False

            if compute_peaks:
                peaks = {'timestamp': [], 'channel_0': []}
                timestamps = np.array(self.windows[metric_name]['timestamps'])
                values = np.array(self.windows[metric_name]['data_to_analyze'])
                peakind = self.compute_peaks(values)
                peaks['timestamp'].extend(list(timestamps[peakind]))
                peaks['channel_0'].extend(list(values[peakind]))

                self.windows[metric_name] = {'timestamps': [],
                                             'data_to_analyze': []}

        return peaks


    def compute_peaks(self, y):
        min = np.min(y)
        max = np.max(y)
        threshold = (min + max) / 2

        return peakutils.indexes(y, thres=threshold)

