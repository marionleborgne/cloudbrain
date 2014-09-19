#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create DataSet"""

__author__ = "marion"

import csv
import os
import numpy


class DataConverter(object):
    """	Format data for the Machine Learning Algos. """

    def format_headers(self, headers):
        formatted_headers = filter(lambda x: x != "timestamp", headers)
        formatted_headers.append("class")
        return formatted_headers

    def convert_api(self, tenant, metric_name, node=True):
        """ Format data retreived from the API """

        pass  # TODO: Format Json string
        return dataset

    def convert_csv(self, path_to_csv_file):
        """ To be overriden"""
        pass


class DTDataConverter(object):
    """
	Return a dataset formmatted like this:
		dataset = [ double, ... , double ]
	"""

    def __init__(self):
        super(DTDataConverter, self).__init__()

    def convert_csv(self, path_to_csv_file):
        """ Format CSV files"""

        reader = DataReader()
        list_of_dictionaries, headers = reader.read_csv(path_to_csv_file)

        dataset = []
        for dictionary in list_of_dictionaries:
            datapoint = []
            for feature in headers:
                if not feature == "timestamp":
                    datapoint.append(float(dictionary[feature]))

            dataset.append(datapoint)

        return dataset


class KOACDataConverter(object):
    """
    Return a dataset formmatted like this:
    dataset = [ scipy.array, ... , scipy.array ]
    """

    def __init__(self):
        super(KOACDataConverter, self).__init__()

    def convert_csv(self, path_to_csv_file, headers_to_exclude):
        """ Format CSV files"""

        reader = DataReader()
        list_of_dictionaries, headers = reader.read_csv(path_to_csv_file)

        dataset = []
        for dictionary in list_of_dictionaries:
            datapoint = []
            for feature in headers:
                if not feature in headers_to_exclude:
                    datapoint.append(float(dictionary[feature]))

            dataset.append(numpy.array(datapoint))

        return dataset


class DataSerializer(object):
    """
	Serialize a dataset.

	Add any function you want, as long as it meets the two following conditions:

	1) Format of input dataset:
		dataset = [ scipy.array, ... , scipy.array ]

	2) Format of dataset headers:
		headers = [feature_1, ..., feature_n]

	"""

    def __init__(self, data_path=None):

        if data_path is not None:
            if not os.path.exists(data_path):
                os.makedirs(data_path)

        self.path = data_path
        self.file = None


    def prepare_csv(self, headers, dataset):

        list_of_dictionaries = []
        for i in range(headers):
            dictionary = {}
            for datapoint in dataset:
                feature = headers[i]
                dictionary[feature] = datapoint[i]
            list_of_dictionaries.append(dictionary)

        return (headers, list_of_dictionaries)


    def write_csv(self, file_name, headers, list_of_dictionaries):
        """ Write CSV file"""

        if self.path is not None:
            self.file = open('%s/%s' % (self.path, file_name), 'wb')
        else:
            self.file = open('%s' % file_name, 'wb')

        csv_writer = csv.DictWriter(self.file, headers, dialect='excel')

        csv_writer.writeheader()
        csv_writer.writerows(list_of_dictionaries)

        self.file.close()


class DataReader(object):
    """
	Read serialised dataset.

	"""


    def read_csv(self, path_to_csv_file):
        """
		This function returns a list of dictionary 
		and the csv headers as a list.

		"""
        csv_file = open('%s' % path_to_csv_file, 'r')

        csv_reader = csv.DictReader(csv_file, dialect='excel')

        list_of_dictionaries = []
        for line in csv_reader:
            list_of_dictionaries.append(line)

        headers = csv_reader.fieldnames

        return (list_of_dictionaries, headers)


class DataStreamer(object):
    """
	Create list of data batches.

	The initial dataset to stream must look like this:

		dataset = [ scipy.array, ... , scipy.array ]

	"""

    def create_batches(self, dataset, batch_size=1):

        data_batches = []
        while len(dataset) > 0:
            data_batch = []
            for i in range(batch_size):
                datapoint = dataset.pop()
                data_batch.append(datapoint)

            data_batches.append(data_batch)

        return data_batches


class Test(object):
    def read_csv(self):
        reader = DataReader()
        list_of_dictionaries, headers = reader.read_csv("../tests/test.csv")

        return (list_of_dictionaries, headers)

    def read_write_csv(self):
        reader = DataReader()
        list_of_dictionaries, headers = reader.read_csv("../tests/test.csv")

        writer = DataSerializer("../tests")
        writer.write_csv("test.csv", headers, list_of_dictionaries)


    def convert_data(self):
        list_of_dictionaries, headers = self.read_csv()

        data_converter = DTDataConverter()
        # data_converter = KOACDataConverter()
        dataset = data_converter.convert_csv("../tests/test.csv")

        return dataset


    def stream_data(self):
        data_path = "../tests/test.csv"

        reader = DataReader()
        list_of_dictionaries, headers = reader.read_csv(data_path)

        data_converter = KOACDataConverter()
        dataset = data_converter.convert_csv(data_path)

        streamer = DataStreamer()
        batch_size = 3
        batches = streamer.create_batches(dataset, batch_size)

        for batch in batches:
            print  "==> NEW BATCH"
            print batch


if __name__ == "__main__":
    test = Test()

    test.read_csv()
    test.read_write_csv()
    test.convert_data()
    test.stream_data()