import numpy as np

from pkg_elastic import fields as fd
from pkg_clustering import dissimilarity as ds


def get_dataset_as_numpy_array(dataset):
    _dataset = []
    for record in dataset:
        _dataset.append(np.asarray(record))
    return _dataset


def region(dataset, p, eps, dissimilarity_matrix):
    neighbors = []

    for point in range(0, len(dataset)):
        if p > point:
            dist = dissimilarity_matrix[p][point]
        else:
            dist = dissimilarity_matrix[point][p]

        if dist < eps:
            neighbors.append(point)

    return neighbors


def expand_cluster(dataset, core_point, neighborhood,
                   core_point_cluster, clusters, eps, min_pts, dissimilarity_matrix):
    clusters[core_point] = core_point_cluster

    i = 0
    while i < len(neighborhood):
        point = neighborhood[i]

        if clusters[point] == -1:
            clusters[point] = core_point_cluster

        elif clusters[point] == 0:
            clusters[point] = core_point_cluster
            point_neighbors = region(dataset, point, eps, dissimilarity_matrix)

            if len(point_neighbors) >= min_pts:
                neighborhood = neighborhood + point_neighbors

        i = i + 1


def run_dbscan(dataset, eps, min_pts, field: fd.Fields):
    dissimilarity_matrix = ds.get_matrix_for_dataset(dataset, field)
    clusters = [0] * len(dataset)
    current_cluster = 0

    for p in range(0, len(dataset)):
        if clusters[p] != 0:
            continue

        neighbors = region(dataset, p, eps, dissimilarity_matrix)
        if len(neighbors) >= min_pts:
            current_cluster = current_cluster + 1
            expand_cluster(dataset, p, neighbors, current_cluster, clusters, eps, min_pts, dissimilarity_matrix)
        else:
            clusters[p] = -1

    return clusters


def show_clusters(clusters):
    i = 0
    for cluster in clusters:
        print(str(i) + " -> " + str(cluster))
        i = i + 1


def get_clusters_dictionary(clusters, dataset):
    dictionary = {}

    for i in range(len(clusters)):
        if clusters[i] in dictionary:
            dictionary[clusters[i]].append(dataset[i])
        else:
            dictionary[clusters[i]] = []
            dictionary[clusters[i]].append(dataset[i])

    return dictionary
