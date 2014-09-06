#!/usr/bin/env python


import sys
import math
import heapq
import operator
import random
import scipy
from numpy import array, linalg
from data import DataReader, DataConverter, DataStreamer

class Cluster(object):

    def __init__(self, center):
        self.center = center
        self.size = 0
        self.datapoints = []

    def __str__(self):
        return "Cluster( %s, %f )" % (self.center, self.size)

    def kernel(self, v, w, sigma=300):
        """Gaussian Kernel"""
        a = v - w
        return math.exp(- linalg.norm(a, ord=2) / (sigma ** 2))

    def kernel_dist(self, v, w):
        """Kernel induced distance"""
        return math.sqrt(self.kernel(v, v) - 2 * self.kernel(v, w) + self.kernel(w, w))

    def add(self, datapoint):
        """Add a new datapoint in the cluster"""

        datapoint = array(datapoint)
        self.datapoints.append(datapoint)
        self.size += self.kernel(self.center, datapoint)
        self.center += (datapoint - self.center) / self.size

    def merge(self, cluster):
        """Merge a cluster with the current cluster"""
        self.center = (self.center * self.size + cluster.center * cluster.size) / (
            self.size + cluster.size)
        self.size += cluster.size

    def resize_center(self, dim):
        """ Zero padding of the centroid of the cluster, if it dimension is inferior to the value'dim' """
        if dim > len(self.center):
            extra = scipy.zeros(dim - len(self.center))
            self.center = scipy.append(self.center, extra)


class KOAC(object):

    """

    K.O.A.C. = Kernel-induced Online Agglomerative Clustering

    __KERNEL__
    * The general idea is to increase the computational power of traditional linear Machine Learning algos
    by mapping the data into a high-dimensional feature space.
    * This technique is usually refered to as the "kernel method" in ML theory.
    * Inspired from the paper: "Improving the robustness of online agglomerative clustering method
    based on kernel-induce distance measures". By Daoqiang Zhang, Songcan Chen, Keren Tan.
    * Which method is doing that? kernel_dist()

    __ONLINE__
    * Just the same principle as an online K-means in N dimensions.
    * Which method is doing that? online_clustering()
    * Stream the data. For each new data point:
      1. Find the closest cluster
      2. Assign the new data point to this cluser
      3. Update the cluster centroid accordingly (because there's now a new data poitn in this cluster)
         Like this: centroid += ( new_datapoint - centroid) / cluster_size
    * Inspired from: http://gromgull.net/blog/2009/08/online-clustering-in-python/

    __AGGLOMERATIVE CLUSTERING__
    * Inspired from the paper: "An on-line agglomerative clustering method for non-stationary data". By I. D. Guedalia, M. London, M. Werman.
    * Which method is doing that? trimclusters()

    """

    def __init__(self, K_max):
        """N is the upper-limit for the number of clusters"""

        self.nb_points_clustered = 0
        self.K_max = K_max 

        self.clusters = []
        # max number of dimensions we've seen so far
        self.dim = 0

        # cache inter-cluster distances
        self.dist = []

    def kernel(self, v, w, sigma=300):
        """Gaussian Kernel"""
        a = array(v) - array(w)
        return math.exp(- linalg.norm(a, ord=2) / (sigma ** 2))

    def kernel_dist(self, v, w):
        """Kernel induced distance"""
        return math.sqrt(self.kernel(v, v) - 2 * self.kernel(v, w) + self.kernel(w, w))

    def resize(self, dim):
        """ Resize each cluster centroid. The method resize_center() is inherited from the class Cluster"""
        for cluster in self.clusters:
            cluster.resize_center(dim)

    def find_closest_cluster(self, datapoint):
        """Find the closest cluster to this datapoint according to the kernel-induced distance"""
        cluster_distances = [(cluster_index, self.kernel_dist(cluster.center, datapoint))
                              for cluster_index, cluster in enumerate(self.clusters)]
        closest_cluster_index = min(
            cluster_distances, key=operator.itemgetter(1))[0]
        closest_cluster = self.clusters[closest_cluster_index]
        return closest_cluster

    def kernel_online_clustering(self, datapoint):


        if len(datapoint) > self.dim:
            self.resize(len(datapoint))
            self.dim = len(datapoint)

        # make a new cluster for this point
        new_cluster = Cluster(datapoint)

        if len(self.clusters) < 1:
            self.clusters.append(new_cluster)
            self.updatedist(new_cluster)

        else:
            closest_cluster = self.find_closest_cluster(datapoint)
            closest_cluster.add(datapoint)
            self.updatedist(closest_cluster) # invalidate dist-cache for this cluster
     
            inter_clusters_distance = self.kernel_dist(new_cluster.center, closest_cluster.center)
            inter_clusters_distances = self.get_inter_cluster_distances()

            if inter_clusters_distance > scipy.mean(inter_clusters_distances):
                self.clusters.append(new_cluster)
                self.updatedist(new_cluster)     


            if len(self.clusters) > self.K_max:
                # merge  two closest clusters
                m = heapq.heappop(self.dist)  # Pop and return the smallest item from the heap
                m.x.merge(m.y)

                self.clusters.remove(m.y)
                self.removedist(m.y)

                self.updatedist(m.x)

            

        self.nb_points_clustered += 1
        return self.clusters

    def get_inter_cluster_distances(self):

        inter_cluster_distances = []
        for cluster1 in self.clusters:
            for cluster2 in self.clusters:
                inter_cluster_distances.append(self.kernel_dist(cluster1.center, cluster2.center))

        return inter_cluster_distances

    def merge_close_clusters(self, inter_cluster_distances):

        inter_cluster_distances = []
        for cluster1 in self.clusters:
            for cluster2 in self.clusters:
                inter_cluster_distance = self.kernel_dist(cluster1.center, cluster2.center)
                if inter_cluster_distance < scipy.mean(inter_cluster_distances):
                    # closest clusters
                    self.merge_clusters(cluster1,cluster2)



    def merge_clusters(self, cluster1, cluster2):
        cluster1.merge(cluster2)
        self.clusters.remove(cluster2)
        self.removedist(cluster2)
        self.updatedist(cluster2)

    def removedist(self, c):
        """invalidate intercluster distance cache"""
        r = []
        for x in self.dist:
            if x.x == c or x.y == c:
                r.append(x)
        for x in r:
            self.dist.remove(x)
        heapq.heapify(self.dist)

    def updatedist(self, new_cluster):
        """Cluster c has changed, re-compute all intercluster distances"""
        self.removedist(new_cluster)

        for cluster in self.clusters:
            if cluster == new_cluster:
                continue
            distance = self.kernel_dist(cluster.center, new_cluster.center)
            cluster_tuple = Tuple(cluster, new_cluster, distance)
            heapq.heappush(self.dist, cluster_tuple)  # push tuple onto the heap

  
    def trimclusters(self):
        """
        Return only clusters over threshold = mean(clusters size) * 0.3
        """
        average_cluster_size = scipy.mean([cluster.size for cluster in filter(
            lambda x: x.size > 0, self.clusters)]) * 0.3
        clusters = filter(lambda x: x.size >= average_cluster_size, self.clusters)
        return clusters



    def cluster(self, datapoint):
        """
        Cluster the new datapoint with KOAC.
        KOAC = Kernel-induced Online Agglomerative Clustering

        """

        self.kernel_online_clustering(datapoint)
        clusters = self.trimclusters()
        return clusters

    def cluster2(self, datapoint):
        """
        Cluster the new datapoint with KOAC.
        KOAC = Kernel-induced Online Agglomerative Clustering

        """

        self.trimclusters2()
        clusters = self.kernel_online_clustering(datapoint)
        return clusters

class Tuple(object):

    """Tuple of vectors that need to be compared """

    def __init__(self, x, y, d):
        """ d is the distance between the vectors x and y"""
        self.x = x
        self.y = y
        self.d = d

    def __cmp__(self, new_tuple):
        """
        Compare the two objects (Tuples) and return an integer according to the outcome.
        * Return a negative integer if self < other
        * Retun 0 if self == other
        * Return a positive integer if self > other.
        This will be used by 'heapq' (priority queue), that needs to compare tuples of vectors.
        """
        return cmp(self.d, new_tuple.d)


class Test(object):

    def generate_data(self):
        """Create 4 random 3D gaussian clusters"""

        dataset = []
        for i in range(4):
            x = random.random() * 5
            y = random.random() * 5
            z = random.random() * 5
            datapoint = [scipy.array((x+random.normalvariate(0,0.1), y+random.normalvariate(0,0.1), z+random.normalvariate(0,0.1))) for j in range(100)]
            dataset += datapoint
        random.shuffle(dataset)

        return dataset

    def run(self):
        """Run test"""

        #import ipdb; ipdb.set_trace()
        dataset = self.generate_data()

        K_max = 10
        koac = KOAC(K_max)
        #import ipdb; ipdb.set_trace()

        while len(dataset) > 0: 

            new_point = dataset.pop()
            clusters = koac.cluster(new_point)

        print "Number of clusters: %s" % str(len(clusters))
        for cluster in clusters:
            print cluster.center

class POC(Test):
   
    def __init__(self): 
        super(POC, self).__init__()

    def generate_data(self):

        data_path = "../tests/test.csv"

        reader = DataReader()
        list_of_dictionaries, headers = reader.read_csv(data_path)

        data_converter = DataConverter("KOAC")
        dataset = data_converter.convert_csv(data_path)

        #streamer = DataStreamer()
        #batch_size = 10
        #batches = streamer.create_batches(dataset, batch_size)

       
        return dataset


if __name__=="__main__":


    #test = Test()
    #test.run()

    poc = POC()
    poc.run()
