import logging
import numpy as np
import unittest
import random

from cloudbrain.modules.transforms.fft import FrequencyBandTransformer

_LOGGER = logging.getLogger(__name__)
_LOGGER.level = logging.DEBUG
_LOGGER.addHandler(logging.StreamHandler())


def generate_sine_wave(number_points,
                       sampling_frequency,
                       alpha_amplitude,
                       alpha_freq,
                       beta_amplitude,
                       beta_freq):
    sample_spacing = 1.0 / sampling_frequency
    x = np.linspace(start=0.0,
                    stop=number_points * sample_spacing,
                    num=number_points)

    alpha = alpha_amplitude * np.sin(alpha_freq * 2.0 * np.pi * x)
    beta = beta_amplitude * np.sin(beta_freq * 2.0 * np.pi * x)

    y = alpha + beta + min(alpha_amplitude,
                           beta_amplitude) / 2.0 * random.random()

    return y



def generate_mock_data(num_channels,
                       number_points,
                       sampling_frequency,
                       buffer_size,
                       alpha_amplitude,
                       alpha_freq,
                       beta_amplitude,
                       beta_freq):
    sine_wave = generate_sine_wave(number_points,
                                   sampling_frequency,
                                   alpha_amplitude,
                                   alpha_freq,
                                   beta_amplitude,
                                   beta_freq)

    buffers = []

    # if number_points = 250 and buffer_size = 40, then num_buffers = 6 + 1
    num_buffers = int(number_points / buffer_size)
    if number_points % buffer_size != 0:
        num_buffers += 1  # you need to account for the almost full buffer

    t0 = 0
    sample_spacing = 1.0 / sampling_frequency
    for i in range(num_buffers):
        if (i + 1) * buffer_size < len(sine_wave):
            y_chunk = sine_wave[i * buffer_size:(i + 1) * buffer_size]
        else:
            y_chunk = sine_wave[i * buffer_size:]

        buffer = []
        for j in range(len(y_chunk)):
            timestamp_in_s = t0 + (buffer_size * i + j) * sample_spacing
            timestamp = int(timestamp_in_s * 1000)

            datapoint = {'timestamp': timestamp}

            for k in range(num_channels):
                datapoint['channel_%s' % k] = y_chunk[j]

            buffer.append(datapoint)

        buffers.append(buffer)

    return buffers



def plot_cb_buffers(num_channels, cb_buffers):
    maxi_buffer = []
    for cb_buffer in cb_buffers:
        maxi_buffer.extend(cb_buffer)
    plot_cb_buffer(num_channels, maxi_buffer)



def plot_cb_buffer(num_channels, cb_buffer):
    import matplotlib.pyplot as plt
    f, axarr = plt.subplots(num_channels)
    for i in range(num_channels):
        channel_name = 'channel_%s' % i
        data_to_plot = []
        for data in cb_buffer:
            data_to_plot.append(data[channel_name])
        axarr[i].plot(data_to_plot)
        axarr[i].set_title(channel_name)
    plt.show()



def generate_frequency_bands(alpha_freq, beta_freq, frequency_band_size):
    """
    Make sure to choose the frequency band size carefully.
    If it is too high, frequency bands will overlap.
    If it's too low, the band might not be large enough to detect the frequency.
    """

    alpha_range = [alpha_freq - frequency_band_size / 2.0,
                   alpha_freq + frequency_band_size / 2.0]
    beta_range = [beta_freq - frequency_band_size / 2.0,
                  beta_freq + frequency_band_size / 2.0]

    frequency_bands = {'alpha': alpha_range, 'beta': beta_range}

    return frequency_bands



class FrequencyBandTranformerTest(unittest.TestCase):
    def setUp(self):

        self.plot_input_data = False

        self.window_size = 250  # Also OK => 2 * 2.50. Or 3 * 250
        self.sampling_freq = 250.0

        self.buffer_size = 10

        self.alpha_amplitude = 10.0
        self.alpha_freq = 10.0

        self.beta_amplitude = 5.0
        self.beta_freq = 25.0

        self.num_channels = 8

        self.freq_band_size = 10.0

        self.number_points = 250

        self.cb_buffers = generate_mock_data(self.num_channels,
                                             self.number_points,
                                             self.sampling_freq,
                                             self.buffer_size,
                                             self.alpha_amplitude,
                                             self.alpha_freq,
                                             self.beta_amplitude,
                                             self.beta_freq)


    def test_cb_buffers(self):

        if self.plot_input_data:
            plot_cb_buffers(self.num_channels, self.cb_buffers)

        num_buffers = self.number_points / self.buffer_size
        if self.window_size % self.buffer_size != 0:
            num_buffers += 1

        self.assertEqual(len(self.cb_buffers), num_buffers)

        self.assertEqual(len(self.cb_buffers[0]), self.buffer_size)
        self.assertTrue('channel_0' in self.cb_buffers[0][0].keys())


    def test_module(self):

        self.frequency_bands = generate_frequency_bands(self.alpha_freq,
                                                        self.beta_freq,
                                                        self.freq_band_size)

        self.subscribers = []
        self.publishers = []

        module = FrequencyBandTransformer(subscribers=self.subscribers,
                                          publishers=self.publishers,
                                          window_size=self.window_size,
                                          sampling_frequency=self.sampling_freq,
                                          frequency_bands=self.frequency_bands)

        for cb_buffer in self.cb_buffers:
            # where the real logic inside the subscriber takes place

            bands = module._compute_fft(cb_buffer, self.num_channels)

            if bands:
                for i in range(self.num_channels):
                    channel_name = 'channel_%s' % i
                    alpha_estimated_ampl = bands['alpha'][channel_name]
                    beta_estimated_ampl = bands['beta'][channel_name]

                    ratio = self.beta_amplitude / self.alpha_amplitude
                    estimated_ratio = beta_estimated_ampl / alpha_estimated_ampl

                    _LOGGER.debug("Alpha: estimated=%s | actual=%s" %
                                  (alpha_estimated_ampl, self.alpha_amplitude))

                    _LOGGER.debug("Beta: estimated=%s | actual=%s" %
                                  (beta_estimated_ampl, self.beta_amplitude))
                    assert np.abs((estimated_ratio - ratio) / ratio) < 0.01
