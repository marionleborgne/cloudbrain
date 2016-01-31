__author__ = 'odrulea'

from cloudbrain.subscribers.PikaSubscriber import PikaSubscriber
from cloudbrain.apps.AnalysisModules import ModuleAbstract
from cloudbrain.utils.metadata_info import get_num_channels, get_supported_metrics, get_supported_devices
from cloudbrain.apps.AnalysisModules.utils import MatrixToBuffer, BufferToMatrix
import json
import numpy as np


class ModuleWindows(ModuleAbstract.ModuleAbstract):
    
    MODULE_NAME = "Windows Module"

    # __init__ is handled by parent ModuleAbstract

    def setup(self):
        ModuleAbstract.ModuleAbstract.setup(self)
        # print self.MODULE_NAME+": setup"

        # init self vars
        # window params
        self.samples_per_second = 1000 # this is unused, just a placeholder for now
        if "samples_per_window" in self.module_params:
            self.samples_per_window = self.module_params["samples_per_window"]
        else:
            self.samples_per_window = 500

        if "window_overlap" in self.module_params:
            self.window_overlap = self.module_params["window_overlap"]
        else:
            self.window_overlap = 100

        if self.debug:
            print "Samples per window:" + str(self.samples_per_window)
            print "Window overlap:" + str(self.window_overlap)

        # usually this module is used with incoming EEG,
        # so we'd like to know num channels, and a header is for convenience
        self.num_channels = get_num_channels(self.device_name,self.input_feature)
        self.headers = ['timestamp'] + ['channel_%s' % i for i in xrange(self.num_channels)]
        # create a blank matrix of zeros as a starting window
        self.window = np.zeros((self.samples_per_window, self.num_channels))
        self.nextWindowSegment = np.zeros((self.window_overlap, self.num_channels))
        self.trimOldWindowDataIndexRange = np.arange(self.window_overlap)

        self.plotActive = True
        self.windowFull = False
        self.fill_counter = 0
        self.rolling_counter = 0




    def consume(self, ch, method, properties, body):
        """
        Windows Module chops streaming multi-channel time series data into 'windows'
        Semantically, window = trial = matrix
        As matrix, window has dimensions [rows, cols] - standard notation for numpy, matlab, etc

        The row captures datum per second
        The column captures datum per channel. Column can represent one channel as a single time-series vector.

        If this were plotted as a time series graph,
        rows = x-axis (time)
        each col = y-axis (voltage)
        You could use this matrix to plot n-channels number of streaming graphs,
        or you could superimpose n-channels number of lines on the same streaming graph
        """

        # begin looping through the buffer coming in from the message queue subscriber
        buffer_content = json.loads(body)

        for record in buffer_content:

            # get the next data out of the buffer as an array indexed by column names
            arr = np.array([record.get(column_name, None) for column_name in self.headers])

            if self.windowFull is False:
                # window is not full yet
                # just keep collecting data into main window until we have filled up the first one
                # i.e. write next row in matrix
                self.window[self.fill_counter, :] = arr[1:len(self.headers)] # note timestamp is not used (i.e. arr[0])
                self.fill_counter = self.fill_counter + 1
                #print "still filling up first window: " + str(self.fill_counter) + " rows so far"

                # once we've reached one full window length, set the flag
                if self.fill_counter == self.samples_per_window:
                    self.windowFull = True
                    if self.debug:
                        print "Received " + str(self.samples_per_window) + " lines:\n"

            else:
                # accumulate every new data into next window segment
                self.nextWindowSegment[self.rolling_counter, :] = arr[1:len(self.headers)]
                # not yet, just keep incrementing rolling counter
                self.rolling_counter = self.rolling_counter + 1

                # check if we have reached next window yet
                if(self.rolling_counter == self.window_overlap):
                    # reached overlap, time to roll over to next window

                    # Step 1: trim off old data rows from the back
                    self.window = np.delete(self.window, self.trimOldWindowDataIndexRange, 0)
                    # Step 2: append next window segment onto the front
                    self.window = np.vstack((self.window, self.nextWindowSegment))

                    # since we've got a new window, time to publish it
                    windowJson = MatrixToBuffer(self.window)
                    self.publisher.publish(windowJson)

                    # since we've rolled to a new window, time to reset the rolling counter
                    self.rolling_counter = 0

                    # debug
                    if self.debug:
                        print self.window
