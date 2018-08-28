import json
import logging
import numpy as np
from scipy import signal

from cloudbrain.modules.interface import ModuleInterface

_LOGGER = logging.getLogger(__name__)



class BandFilter(ModuleInterface):
    def __init__(self,
                 subscribers,
                 publishers,
                 filter_type,
                 start_frequency,
                 stop_frequency,
                 sampling_frequency):

        super(BandFilter, self).__init__(subscribers, publishers)
        _LOGGER.debug("Subscribers: %s" % self.subscribers)
        _LOGGER.debug("Publishers: %s" % self.publishers)

        self.filter_type = filter_type
        self.start_frequency = start_frequency
        self.stop_frequency = stop_frequency
        self.window_size = 50

        # Filter params
        f_nyquist = 0.5 * sampling_frequency
        f_start = self.start_frequency / f_nyquist
        f_stop = self.stop_frequency / f_nyquist

        self.a, self.b = signal.butter(1, [f_start, f_stop], self.filter_type)

        # Keep a window of points for the filter - usually it is good practice
        # to discard the first ~50 points
        sliding_window = np.zeros(self.window_size)
        self.sliding_windows = [{} for subscriber in self.subscribers]
        for i in range(len(self.subscribers)):
            subscriber = self.subscribers[i]
            metrics_to_num_channels = subscriber.metrics_to_num_channels()
            for (metric_name, num_channels) in metrics_to_num_channels.items():
                self.sliding_windows[i][metric_name] = {
                    'channel_%s' % i: sliding_window
                    for i in range(num_channels)}


    def start(self):
        for i in range(len(self.subscribers)):
            subscriber = self.subscribers[i]
            for sub_metric_buffer in subscriber.metric_buffers.values():
                sub_metric_name = sub_metric_buffer.name
                sub_num_channels = sub_metric_buffer.num_channels

                sliding_window = self.sliding_windows[i][sub_metric_name]

                for publisher in self.publishers:
                    for pub_metric_buffer in publisher.metric_buffers.values():
                        pub_metric_name = pub_metric_buffer.name
                        callback = self._callback_factory(sub_num_channels,
                                                          publisher,
                                                          pub_metric_name,
                                                          self.a,
                                                          self.b,
                                                          sliding_window)

                        subscriber.subscribe(sub_metric_name, callback)


    def _callback_factory(self,
                          sub_num_channels,
                          publisher,
                          pub_metric_name,
                          a,
                          b,
                          metrics_sliding_window):

        def callback(unused_ch,
                     unused_method,
                     unused_properties,
                     data):

            cb_buffer = json.loads(data)
            filtered_buffer = self._filter(cb_buffer,
                                           sub_num_channels,
                                           a,
                                           b,
                                           metrics_sliding_window)
            for filtered_data in filtered_buffer:
                publisher.publish(pub_metric_name, filtered_data)


        return callback


    def _filter(self, cb_buffer, num_channels, a, b, metrics_sliding_window):

        filtered_buffer = []
        for data in cb_buffer:
            filtered_data = {'timestamp': data['timestamp']}
            for i in range(num_channels):
                channel_name = 'channel_%s' % i

                # push to the left
                metrics_sliding_window[channel_name] = np.append(
                    metrics_sliding_window[channel_name][1:],
                    data[channel_name])

                win = metrics_sliding_window[channel_name]
                result = signal.lfilter(a, b, win)
                filtered_data[channel_name] = result[-1]
            filtered_buffer.append(filtered_data)

        return filtered_buffer
