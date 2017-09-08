# -*- coding: utf-8 -*-

"""
Copyright Puzzlebox Productions, LLC (2010-2016)

Ported from Puzzlebox Synapse
ThinkGear code imported from Puzzlebox.Synapse.ThinkGear.Server
http://puzzlebox.io

This code is released under the GNU Pulic License (GPL) version 3
For more information please refer to http://www.gnu.org/copyleft/gpl.html

Author: Steve Castellotti <sc@puzzlebox.io>
"""

__changelog__ = """Last Update: 2017.05.28"""
import threading
import signal
import sys

from cloudbrain.connectors.thinkgear import SerialDevice
from cloudbrain.connectors.thinkgear import puzzlebox_synapse_protocol_thinkgear

THINKGEAR_DEVICE_SERIAL_PORT = '/dev/tty.MindWaveMobile-DevA'
VALID_METRICS = ['eeg', 'poorSignalLevel', 'attention', 'meditation', 'delta',
                 'theta', 'lowAlpha', 'highAlpha', 'lowBeta', 'highBeta',
                 'lowGamma', 'highGamma']


def displayCSVHeader():
    print("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
        'timestamp',
        'eeg',
        'poorSignalLevel',
        'attention',
        'meditation',
        'delta',
        'theta',
        'lowAlpha',
        'highAlpha',
        'lowBeta',
        'highBeta',
        'lowGamma',
        'highGamma'))


def displayCSV(packet):
    print("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
        packet['timestamp'],
        packet['eeg'],
        packet['poorSignalLevel'],
        packet['attention'],
        packet['meditation'],
        packet['delta'],
        packet['theta'],
        packet['lowAlpha'],
        packet['highAlpha'],
        packet['lowBeta'],
        packet['highBeta'],
        packet['lowGamma'],
        packet['highGamma']))


class NeuroskyConnector(threading.Thread):
    def __init__(self, callback_functions,
                 device_address=THINKGEAR_DEVICE_SERIAL_PORT,
                 verbosity=0):

        self.parent = None
        self.protocol = None
        self.serial_device = None
        self.log = None
        self.verbosity = verbosity

        threading.Thread.__init__(self, self.parent)

        self.device_address = device_address

        self.data = {
            'poorSignalLevel': 200, 'attention': 0, 'meditation': 0, 'delta': 0,
            'theta': 0, 'lowAlpha': 0, 'highAlpha': 0, 'lowBeta': 0,
            'highBeta': 0, 'lowGamma': 0, 'highGamma': 0
        }

        for metric in callback_functions.keys():
            if metric not in VALID_METRICS:
                raise ValueError('Output metric is set to "%s" but must be in '
                                 'the valid metrics list: %s' % (metric,
                                                                 VALID_METRICS))

        self.callback_functions = callback_functions

        # Final setup
        self.configureEEG()
        self.displayCSVHeader = True

        print("Attempting to connect to NeuroSky headset ...")
        print("WARNING: Make sure the headset is on, paired, and "
              "has enough battery.")

    def setPacketCount(self, value):

        if self.parent is not None:
            self.parent.setPacketCount(value)

    def setBadPackets(self, value):

        if self.parent is not None:
            self.parent.setBadPackets(value)

    def incrementPacketCount(self):

        if self.parent is not None:
            self.parent.incrementPacketCount()

    def incrementBadPackets(self):

        if self.parent is not None:
            self.parent.incrementBadPackets()

    def resetSessionStartTime(self):

        if self.parent is not None:
            self.parent.resetSessionStartTime()

    def configureEEG(self):

        self.serial_device = SerialDevice(
            self.log,
            device_address=self.device_address,
            DEBUG=0,
            parent=self)

        self.serial_device.start()

        self.protocol = puzzlebox_synapse_protocol_thinkgear(
            self.log,
            self.serial_device,
            device_model='NeuroSky MindWave',
            DEBUG=0,
            parent=self)

        self.protocol.start()

    def processPacketThinkGear(self, packet):

        if self.displayCSVHeader:
            displayCSVHeader()
            self.displayCSVHeader = False

        if self.verbosity >= 2:
            print(packet)

        if 'rawEeg' in packet.keys():

            packet['eeg'] = packet.pop('rawEeg')
            packet['poorSignalLevel'] = self.data['poorSignalLevel']
            packet['attention'] = self.data['attention']
            packet['meditation'] = self.data['meditation']
            packet['delta'] = self.data['delta']
            packet['theta'] = self.data['theta']
            packet['lowAlpha'] = self.data['lowAlpha']
            packet['highAlpha'] = self.data['highAlpha']
            packet['lowBeta'] = self.data['lowBeta']
            packet['highBeta'] = self.data['highBeta']
            packet['lowGamma'] = self.data['lowGamma']
            packet['highGamma'] = self.data['highGamma']

            if self.verbosity >= 1:
                displayCSV(packet)

            for metric, callback in self.callback_functions.items():
                callback(packet['timestamp'], packet[metric])

        else:
            if 'poorSignalLevel' in packet.keys():
                self.data['poorSignalLevel'] = packet['poorSignalLevel']

            if 'eegPower' in packet.keys():
                self.data['delta'] = packet['eegPower']['delta']
                self.data['theta'] = packet['eegPower']['theta']
                self.data['lowAlpha'] = packet['eegPower']['lowAlpha']
                self.data['highAlpha'] = packet['eegPower']['highAlpha']
                self.data['lowBeta'] = packet['eegPower']['lowBeta']
                self.data['highBeta'] = packet['eegPower']['highBeta']
                self.data['lowGamma'] = packet['eegPower']['lowGamma']
                self.data['highGamma'] = packet['eegPower']['highGamma']

            if 'eSense' in packet.keys():
                if 'attention' in packet['eSense'].keys():
                    self.data['attention'] = packet['eSense']['attention']
                if 'meditation' in packet['eSense'].keys():
                    self.data['meditation'] = packet['eSense']['meditation']

    def resetDevice(self):

        if self.serial_device is not None:
            self.serial_device.exitThread()

        if self.protocol is not None:
            self.protocol.exitThread()

        self.configureEEG()

    def exitThread(self, callThreadQuit=True):

        # Call disconnect block in protocol first due to above error
        self.protocol.disconnectHardware()

        if self.serial_device is not None:
            self.serial_device.exitThread()

        if self.protocol is not None:
            self.protocol.exitThread()

        if callThreadQuit:
            self.join()

        if self.parent is None:
            sys.exit()


def callback_factory(metric_name):
    def print_callback(timestamp, sample):
        print('metric_name=%s, timestamp=%s, sample=%s' % (metric_name,
                                                           timestamp, sample))

    return print_callback


def run(device_address=THINKGEAR_DEVICE_SERIAL_PORT):
    """Run the NeuroskyConnector."""

    # Perform correct KeyboardInterrupt handling
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    callbacks = {metric: callback_factory(metric) for metric in VALID_METRICS}

    connector = NeuroskyConnector(
        callback_functions=callbacks,
        device_address=device_address)

    connector.start()


if __name__ == "__main__":
    run()
