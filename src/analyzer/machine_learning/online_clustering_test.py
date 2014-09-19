#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Marion LeBorgne"
__email__ = "marion@ebrain.io"
__version__ = "1.0"

"""Real-time Pattern Detection"""

from data import DataReader, KOACDataConverter, DataStreamer
from unsupervised_learning import KOAC


def get_batches():

    data_path = "../data/jim_10filt_clean.csv"

    data_converter = KOACDataConverter()
    headers_to_exclude = ["time", "tag"]
    dataset = data_converter.convert_csv(data_path, headers_to_exclude)

    streamer = DataStreamer()
    batch_size = 1
    batches = streamer.create_batches(dataset, batch_size)

    return batches

def cluster(K_max):

    batches = get_batches()

    koac = KOAC(K_max)
    for batch in batches:

        #print batches.index(batch)
        while len(batch) > 0:
            new_point = batch.pop()
            clusters = koac.cluster(new_point)


    print "Number of clusters: %s" % str(len(clusters))

    return clusters

if __name__ == '__main__':
    K_max = 4 # upper bound for the number clusters to detect
    clusters = cluster(K_max)

    for cluster in clusters:
        print cluster
