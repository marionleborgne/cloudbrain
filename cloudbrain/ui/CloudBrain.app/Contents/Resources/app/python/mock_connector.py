#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys, json, time, random

_NUM_CHANNELS = 8

while 1:
  timestamp = time.time() * 1000
  message = {'user_id': 'mock_user'}
  message['eeg'] = {'timestamp': timestamp}
  message['powerBands'] = {'timestamp': timestamp}
  for i in xrange(_NUM_CHANNELS):
    channel_id = "channel_%s" %i
    message['eeg'][channel_id] = random.random() * 10
    message['powerBands']['alpha'] = random.random() * 10
    message['powerBands']['beta'] = random.random() * 10
    message['powerBands']['gamma'] = random.random() * 10
    message['powerBands']['theta'] = random.random() * 10
    message['powerBands']['delta'] = random.random() * 10


  print (json.dumps(message))
  sys.stdout.flush()
  time.sleep(0.5)
