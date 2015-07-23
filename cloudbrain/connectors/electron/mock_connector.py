#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys, json, time, random


"""
{
    "channel_0": {
        "alpha": {
            "timestamp": 1437628679947.953, 
            "value": 3.7259920070884576
        }, 
        "beta": {
            "timestamp": 1437628679947.953, 
            "value": 8.830775031204494
        }, 
        "delta": {
            "timestamp": 1437628679947.953, 
            "value": 8.565266491998585
        }, 
        "eeg": {
            "timestamp": 1437628679947.953, 
            "value": 9.278570344369484
        }, 
        "gamma": {
            "timestamp": 1437628679947.953, 
            "value": 4.743549273535667
        }, 
        "theta": {
            "timestamp": 1437628679947.953, 
            "value": 6.147279092246158
        }
    }, 
    
    ...
     
    "channel_3": {
        "alpha": {
            "timestamp": 1437628679947.953, 
            "value": 3.1277985131928254
        }, 
        "beta": {
            "timestamp": 1437628679947.953, 
            "value": 7.716722826658473
        }, 
        "delta": {
            "timestamp": 1437628679947.953, 
            "value": 9.62622950791564
        }, 
        "eeg": {
            "timestamp": 1437628679947.953, 
            "value": 7.919877774310157
        }, 
        "gamma": {
            "timestamp": 1437628679947.953, 
            "value": 2.232999212112725
        }, 
        "theta": {
            "timestamp": 1437628679947.953, 
            "value": 8.893638624696042
        }
    }, 
    "user_id": "mock_user"
}
"""

_NUM_CHANNELS = 4

while 1:
  timestamp = time.time() * 1000
  message = {'user_id': 'mock_user'}
  for i in xrange(_NUM_CHANNELS):
    channel_id = "channel_%s" %i
    message[channel_id] = {}
    message[channel_id]['eeg'] = {'timestamp': timestamp, 'value': random.random() * 10}
    message[channel_id]['alpha'] = {'timestamp': timestamp, 'value': random.random() * 10}
    message[channel_id]['beta'] = {'timestamp': timestamp, 'value': random.random() * 10}
    message[channel_id]['theta'] = {'timestamp': timestamp, 'value': random.random() * 10}
    message[channel_id]['gamma'] = {'timestamp': timestamp, 'value': random.random() * 10}
    message[channel_id]['delta'] = {'timestamp': timestamp, 'value': random.random() * 10}

  print (json.dumps(message))
  sys.stdout.flush()
  time.sleep(0.5)
