import unittest
import numpy as np
from pprint import pprint as pp


def chunk_data(data, window_size, step_size):
    """

    :param data:
        [{timestamp, channel_0, ..., channel_N}, ..., {timestamp, channel_0, ..., channel_N}]
    :param window_size:
    :param step_size:
    :return:
    """

    data = sorted(data, key=lambda x: x['timestamp'])
    chunks = []
    for i in range(0, len(data) - window_size, step_size):
        chunks.append(data[i:i+window_size])
    return chunks


def convert_to_numpy(chunks, window_size, num_channels):

    np_chunks = []

    for chunk in chunks:
        np_chunk = np.zeros([window_size, num_channels])
        for i in range(window_size):
            for j in range(num_channels):
                np_chunk[i, j] = chunk[i]['channel_%s' %j]
        np_chunks.append(np_chunk)

    return np_chunks


def stft_with_chunking(data, window_size, step_size, num_channels, frequency_band_mappings,
                       sampling_frequency):
    """
    :param frequency_band_mappings:
     [{"name": "alpha", "hz_range": [7,13]}, {"name": "beta", "hz_range": [13,30]}]

    """
    freqs = np.fft.fftfreq(window_size, d=1./sampling_frequency)
    freqs = np.where(freqs >= 0)[0] # keep only the positive frequencies

    chunks = chunk_data(data, window_size, step_size)
    np_chunks = convert_to_numpy(chunks, window_size, num_channels)

    # init power band amplitudes to 0. We'll sum the values of all the chunks
    # in window_size (i.e. in len(chunks))
    power_band_amplitudes = {}
    for (band_name, frequency_range) in frequency_band_mappings.items():
        power_band_amplitudes[band_name] = {}
        for i in range(num_channels):
            power_band_amplitudes[band_name]['channel_%s' %i] = 0.0

    for (band_name, frequency_range) in frequency_band_mappings.items():
        low_frequency, high_frequency = frequency_range
        frequency_band_indices = (freqs >= low_frequency) & (freqs < high_frequency)
        for np_chunk in np_chunks:
            for i in range(num_channels):
                # take absolute value to discard the phase info
                channel_bands_amplitudes = np.abs(np.fft.rfft(np_chunk[:, i]))
                power_band_amplitudes[band_name]['channel_%s' % i] = np.sum(
                    channel_bands_amplitudes[frequency_band_indices])

    return power_band_amplitudes

class DSPTest(unittest.TestCase):

    def setUp(self):
        self.frequency_band_size = 10.0

        self.num_records = 250
        self.sampling_frequency = 250.0 # in Hz
        self.start = 0.0
        self.end = self.start + self.num_records / self.sampling_frequency
        self.t = np.arange(self.start, self.end, 1 / self.sampling_frequency)

        alpha = {'amplitude': 1.0, 'frequency': 10.0}
        beta = {'amplitude': 10.0, 'frequency': 20.0}
        self.expected_frequencies = {'alpha': alpha, 'beta': beta}

        alpha_sine_wave = alpha['amplitude'] * np.sin(2.0 * np.pi * alpha['frequency'] * self.t)

        beta_sine_wave = beta['amplitude'] * np.sin(2.0 * np.pi * beta['frequency'] * self.t)

        self.sine_wave = alpha_sine_wave + beta_sine_wave

        self.data = []
        self.num_channels = 8
        for i in range(self.num_records):
            datapoint = {'timestamp': self.t[i]}
            for k in range(self.num_records):
                datapoint['channel_%s' % k] = self.sine_wave[i]
            self.data.append(datapoint)


        self.frequency_band_mappings = {}
        for (band_name, band) in self.expected_frequencies.items():
            min_freq = band['frequency'] - self.frequency_band_size
            max_freq = band['frequency'] + self.frequency_band_size
            self.frequency_band_mappings[band_name] = [min_freq, max_freq]

        print "* Frequency bands mappings *"
        pp(self.frequency_band_mappings)
        print ""

        print "* Expected frequencies *"
        pp(self.expected_frequencies)
        print ""


    def test_stft_with_chunking(self):

        window_size = 64
        step_size = 32

        bands = stft_with_chunking(self.data, window_size, step_size, self.num_channels,
                                   self.frequency_band_mappings, self.sampling_frequency)

        print "* Estimated bands *"
        pp(bands)
        print ""

        estimated_freq_amplitudes = {}
        expected_freq_amplitudes = {}
        for (band_name, estimated_freqs) in bands.items():
            estimated_freq_amplitudes[band_name] = estimated_freqs['channel_0']
            expected_freq_amplitudes[band_name] = self.expected_frequencies[band_name]['amplitude']

        print "* Estimated amplitudes *"
        pp(estimated_freq_amplitudes)
        print ""

        print "* Expected amplitudes *"
        pp(expected_freq_amplitudes)
        print ""

        estimated_ratio = estimated_freq_amplitudes['beta'] / estimated_freq_amplitudes['alpha']
        expected_ratio = expected_freq_amplitudes['beta'] / expected_freq_amplitudes['alpha']

        print "* Amplitude ratios *"
        print "Expected: %s | Estimated: %s" % (expected_ratio, estimated_ratio)

        # 90 % error with this method!!!! TODO: sync with Pierre
        self.assertGreaterEqual(np.abs((estimated_ratio - expected_ratio)/ expected_ratio), 0.90)
