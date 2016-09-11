import mne
from mne.io import RawArray
from mne import create_info

import numpy as np

import json
import logging

from cloudbrain.modules.interface import ModuleInterface

_LOGGER = logging.getLogger(__name__)



class BPMTransformer(ModuleInterface):

    """
    The BPM transformer analyzes only one channel per device and per metric.
    Note that this must be the same channel number across all subscribers.
    This means that you need to subscribe to the same device/metric so that the channel number is
    consistent.
    """
    def __init__(self, subscribers, publishers, window_size, channel_number):

        super(BPMTransformer, self).__init__(subscribers, publishers)
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

                self.windows[metric_name] = {'timestamps': [], 'data_to_analyze': []}

                callback = self._callback_factory(metric_name)
                subscriber.subscribe(metric_buffer.name, callback)


    def _callback_factory(self, metric_name):

        publishers = self.publishers


        def process_metric(unused_ch, unused_method, unused_properties, body):

            bpm = self._find_bpm(json.loads(body), metric_name)

            if bpm:
                for publisher in publishers:
                    for pub_metric_buffer in publisher.metric_buffers.values():
                        pub_metric_name = pub_metric_buffer.name
                        publisher.publish(pub_metric_name, bpm)
                        print bpm


        return process_metric


    def _find_bpm(self, cb_buffer, metric_name):
        """

        :param cb_buffer:
        :param metric_name:
        :param num_channels:
        :return bpm: (float)
        """

        bpm = None
        for data in cb_buffer:

            self.windows[metric_name]['data_to_analyze'].append(data[self.channel_name] * 1000)
            self.windows[metric_name]['timestamps'].append(data['timestamp'])
            if len(self.windows[metric_name]['timestamps']) == self.window_size:
                compute_peaks = True
            else:
                compute_peaks = False

            if compute_peaks:
                timestamps = np.array(self.windows[metric_name]['timestamps'])
                timestamps_in_s = timestamps / 1000000.0 # microsec to sec
                values = self.windows[metric_name]['data_to_analyze']
                avg_bpm = self.compute_bpm(values)
                # avg_time_delta = np.mean(np.diff(timestamps_in_s[peakind]))
                # avg_bpm = 60 / avg_time_delta
                bpm = {'timestamp': timestamps[0], 'channel_0': int(avg_bpm)}

                self.windows[metric_name] = {'timestamps': [], 'data_to_analyze': []}

        return bpm


    def compute_bpm(self, y):
        raw = RawArray(np.array([y]), create_info(['channel_0'], 250.0, ch_types=['grad']))
        ecg_epochs = mne.preprocessing.find_ecg_events(raw)
        bpm = ecg_epochs[2]
        return bpm
