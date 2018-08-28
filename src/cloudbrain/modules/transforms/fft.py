import logging
import json

import numpy as np
from scipy.fftpack import fft
from scipy.signal import kaiser

from cloudbrain.modules.interface import ModuleInterface

_LOGGER = logging.getLogger(__name__)



class FrequencyBandTransformer(ModuleInterface):
    def __init__(self, subscribers, publishers, window_size, sampling_frequency,
                 frequency_bands):

        super(FrequencyBandTransformer, self).__init__(subscribers, publishers)
        _LOGGER.debug("Subscribers: %s" % self.subscribers)
        _LOGGER.debug("Publishers: %s" % self.publishers)

        self.data_to_analyze = {'channel_%s' % i: []
                                for i in range(window_size)}
        self.window_size = window_size
        self.sampling_frequency = sampling_frequency
        self.frequency_bands = frequency_bands

        # TODO: should window_size be a multiple of sampling_frequency?
        # Should it be higher? and window_size > sampling_frequency
        # assert self.window_size % self.sampling_frequency == 0
        # assert self.window_size >= self.sampling_frequency


    def start(self):
        for subscriber in self.subscribers:
            for metric_buffer in subscriber.metric_buffers.values():
                num_channels = metric_buffer.num_channels
                callback = self._callback_factory(num_channels)
                subscriber.subscribe(metric_buffer.name, callback)


    def _callback_factory(self, num_channels):

        publishers = self.publishers


        def process_metric(unused_ch, unused_method, unused_properties, body):

            bands = self._compute_fft(json.loads(body), num_channels)

            if bands:
                for (band_name, values) in bands.items():
                    for publisher in publishers:
                        publisher.publish(band_name, values)


        return process_metric


    def _compute_fft(self, cb_buffer, num_channels):

        bands = None
        for data in cb_buffer:

            timestamp = data['timestamp']
            for i in range(num_channels):
                channel_name = 'channel_%s' % i
                self.data_to_analyze[channel_name].append(data[channel_name])
                if len(self.data_to_analyze[channel_name]) == self.window_size:
                    compute_fft = True
                else:
                    compute_fft = False

            if compute_fft:
                bands = {}
                for i in range(num_channels):
                    channel_name = 'channel_%s' % i
                    channel_data = self.data_to_analyze[channel_name]
                    data_to_analyze = np.array(channel_data)
                    channel_bands = self.compute_freq_bands(data_to_analyze)
                    for (band_name, band_value) in channel_bands.items():
                        if band_name not in bands:
                            bands[band_name] = {'timestamp': timestamp}
                        bands[band_name][channel_name] = band_value

                self.data_to_analyze = {'channel_%s' % i: []
                                        for i in range(self.window_size)}

        return bands


    def compute_freq_bands(self, y):
        """
        Compute FFT using a kaiser window over a series of data points of
        length window_size.

        The Kaiser window can approximate many other windows by varying
        the beta parameter.

        beta  |  Window shape
        ------------------------------
        0	  |  Rectangular
        5	  |  Similar to a Hamming
        6	  |  Similar to a Hann
        8.6	  |  Similar to a Blackman

        A beta value of 14 is probably a good starting point.
        Note that as beta gets large, the window narrows, and so the number
        of samples needs
        to be large enough to sample the increasingly narrow spike,
        otherwise NaNs will get returned.

        More here:
        http://docs.scipy.org/doc/scipy-0.17.0/reference/generated/
        scipy.signal.kaiser.html

        :param y: (numpy.Array) array of floats. Frequency bands will be
            extracted from this data.
        """

        # make sure the number of data points to analyze is equal to window size
        assert len(y) == self.window_size

        w = kaiser(self.window_size, beta=14)
        ywf = fft(y * w)

        freqs = np.fft.fftfreq(self.window_size, d=1. / self.sampling_frequency)

        bands = {}
        for (name, freq_range) in self.frequency_bands.items():
            bands[name] = np.sum(np.abs(ywf[(freqs >= freq_range[0])
                                            & (freqs < freq_range[1])]))

        return bands
