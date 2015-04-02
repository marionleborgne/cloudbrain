#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------
"""
Groups together code used for creating a NuPIC model and dealing with IO.
"""
import importlib
import time
import datetime
import json
import sys
import socket

from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.modelfactory import ModelFactory

from cloudbrain.analyzer.htm.example import nupic_anomaly_output


METRIC_NAME = "openbci"
DATA_DIR = "."
MODEL_PARAMS_DIR = "./model_params"
# '7/2/10 0:00'
DATE_FORMAT = "%m/%d/%Y %H:%M:%S:%f"
# BCI Server info
IP = 'localhost'
PORT = 5555


def createModel(modelParams):
  """
  Given a model params dictionary, create a CLA Model. Automatically enables
  inference for metric_value.
  :param modelParams: Model params dict
  :return: OPF Model object
  """
  model = ModelFactory.create(modelParams)
  model.enableInference({"predictedField": "metric_value"})
  return model



def getModelParamsFromName(metric_name):
  """
  Given a metric name, assumes a matching model params python module exists within
  the model_params directory and attempts to import it.
  :param metric_name: metric name, used to guess the model params module name.
  :return: OPF Model params dictionary
  """
  importName = "model_params.%s" % (
    metric_name.replace(" ", "_").replace("-", "_")
  )
  print "Importing model params from %s" % importName
  try:
    importedModelParams = importlib.import_module(importName).MODEL_PARAMS
  except ImportError:
    raise Exception("No model params exist for '%s'. Run swarm first!"
                    % metric_name)
  return importedModelParams



def runIoThroughNupic(ip, port, model, metric_name, plot):
  """
  Handles looping over the input data and passing each row into the given model
  object, as well as extracting the result object and passing it into an output
  handler.
  :param ip: IP address of the muse server
  :param port: port of the muse server
  :param model: OPF Model object
  :param metric_name: metric name, used for output handler naming
  :param plot: Whether to use matplotlib or not. If false, uses file output.
  """
  client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  client.bind((ip, port))

  shifter = InferenceShifter()
  if plot:
    output = nupic_anomaly_output.NuPICPlotOutput(metric_name)
  else:
    output = nupic_anomaly_output.NuPICFileOutput(metric_name)

  counter = 0
  while 1:
    counter += 1
    if (counter % 100 == 0):
      print "Read %i lines..." % counter

    data = json.loads(client.recv(1024))
    print data
    # data in nano-volts (10E9)
    metric_value = float(data['channel_values'][0] * 10E8)
    result = model.run({
      "metric_value": metric_value
    })
    #print metric_value

    if plot:
      result = shifter.shift(result)

    prediction = result.inferences["multiStepBestPredictions"][1]
    anomalyScore = result.inferences["anomalyScore"]

    # TODO: timestamp data BEFORE sending it.
    t = datetime.datetime.now().strftime(DATE_FORMAT)
    timestamp = datetime.datetime.strptime(t, DATE_FORMAT)

    # write output
    output.write(timestamp, metric_value, prediction, anomalyScore)

  output.close()



def runModel(metric_name, plot=False):
  """
  Assumes the metric Name corresponds to both a like-named model_params file in the
  model_params directory.
  :param metric_name: Important for finding model params
  :param plot: Plot in matplotlib? Don't use this unless matplotlib is
  installed.
  """
  print "Creating model from %s..." % metric_name
  model = createModel(getModelParamsFromName(metric_name))
  runIoThroughNupic(IP, PORT, model, metric_name, plot)


if __name__ == "__main__":
  plot = True
  args = sys.argv[1:]
  if "--noplot" in args:
    plot = False
  runModel(METRIC_NAME, plot=plot)