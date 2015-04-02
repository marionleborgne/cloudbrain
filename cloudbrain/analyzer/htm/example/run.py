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
import sys
import csv
import datetime


from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.modelfactory import ModelFactory

from cloudbrain.analyzer.htm.example import nupic_anomaly_output


DESCRIPTION = (
  "Starts a NuPIC model from the model params returned by the swarm\n"
  "and pushes each line of input from the CSV into the model. Results\n"
  "are written to an output file (default) or plotted dynamically if\n"
  "the --plot option is specified.\n"
)
CSV_NAME = "scalar_data"
DATA_DIR = "."
MODEL_PARAMS_DIR = "./model_params"
# '7/2/10 0:00'
DATE_FORMAT = "%m/%d/%y %H:%M"


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



def getModelParamsFromName(csvName):
  """
  Given a csv name, assumes a matching model params python module exists within
  the model_params directory and attempts to import it.
  :param csvName: CSV name, used to guess the model params module name.
  :return: OPF Model params dictionary
  """
  importName = "model_params.%s_model_params" % (
    csvName.replace(" ", "_").replace("-", "_")
  )
  print "Importing model params from %s" % importName
  try:
    importedModelParams = importlib.import_module(importName).MODEL_PARAMS
  except ImportError:
    raise Exception("No model params exist for '%s'. Run swarm first!"
                    % csvName)
  return importedModelParams



def runIoThroughNupic(inputData, model, csvName, plot):
  """
  Handles looping over the input data and passing each row into the given model
  object, as well as extracting the result object and passing it into an output
  handler.
  :param inputData: file path to input data CSV
  :param model: OPF Model object
  :param csvName: CSV name, used for output handler naming
  :param plot: Whether to use matplotlib or not. If false, uses file output.
  """
  inputFile = open(inputData, "rb")
  csvReader = csv.reader(inputFile)
  # skip header rows
  csvReader.next()
  csvReader.next()
  csvReader.next()

  shifter = InferenceShifter()
  if plot:
    output = nupic_anomaly_output.NuPICPlotOutput(csvName)
  else:
    output = nupic_anomaly_output.NuPICFileOutput(csvName)

  counter = 0
  for row in csvReader:
    counter += 1
    if (counter % 100 == 0):
      print "Read %i lines..." % counter
    timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
    consumption = float(row[1])
    result = model.run({
      "timestamp": timestamp,
      "metric_value": consumption
    })

    if plot:
      result = shifter.shift(result)

    prediction = result.inferences["multiStepBestPredictions"][1]
    anomalyScore = result.inferences["anomalyScore"]
    output.write(timestamp, consumption, prediction, anomalyScore)

  inputFile.close()
  output.close()



def runModel(csvName, plot=False):
  """
  Assumes the CSV Name corresponds to both a like-named model_params file in the
  model_params directory, and that the data exists in a like-named CSV file in
  the current directory.
  :param csvName: Important for finding model params and input CSV file
  :param plot: Plot in matplotlib? Don't use this unless matplotlib is
  installed.
  """
  print "Creating model from %s..." % csvName
  model = createModel(getModelParamsFromName(csvName))
  inputData = "%s/%s.csv" % (DATA_DIR, csvName.replace(" ", "_"))
  runIoThroughNupic(inputData, model, csvName, plot)



if __name__ == "__main__":
  print DESCRIPTION
  plot = True
  args = sys.argv[1:]
  if "--noplot" in args:
    plot = False
  runModel(CSV_NAME, plot=plot)