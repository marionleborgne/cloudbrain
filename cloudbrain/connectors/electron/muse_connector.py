#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys, json, time, random

while 1:
  timestamp = time.time() * 1000
  value_0 = random.random() * 10
  value_1 = random.random() * 10
  value_2 = random.random() * 10
  value_3 = random.random() * 10
  alpha = random.random() * 10
  beta = random.random() * 10
  theta = random.random() * 10
  gamma = random.random() * 10
  delta = random.random() * 10
  
  message = {'eeg' : {'user_id': 'test',
                      'timestamp': timestamp, 
                      'value_0': value_0, 
                      'value_1' : value_1, 
                      'value_2': value_2, 
                      'value_3': value_3},
             'power_bands': {'user_id': 'test',
                             'timestamp': alpha,
                             'alpha': alpha,
                             'beta': beta,
                             'gamma': gamma,
                             'theta': theta,
                             'delta': delta
                             }
             
             }

  print (json.dumps(message))
  sys.stdout.flush()
  time.sleep(0.5)
