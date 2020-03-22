import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
import igraph as ig
from shapely.geometry import box
import osmnx as ox


def edge_length_stats(graph):

    lengths = np.array([x['length'] for _, x in graph.edges.items()])
    mean = lengths.mean()
    sigma = lengths.std()

    return {'edge_length_avg':mean, 'edge_length_std':sigma}


def degree_stats(graph):

    in_degrees = np.array([d for e, d in graph.in_degree])
    in_mean = in_degrees.mean()
    in_sigma = in_degrees.std()

    out_degrees = np.array([d for e, d in graph.out_degree])
    out_mean = out_degrees.mean()
    out_sigma = out_degrees.std()

    return {'in_degree_avg':in_mean, 'in_degree_std':in_sigma,
            'out_degree_avg':out_mean, 'out_degree_std':out_sigma}


def compute_paths(graph, origin):
    G_ig = ig.Graph(directed=True)

    G_ig.add_vertices(list(graph.nodes()))
    G_ig.add_edges(list(graph.edges()))

    # G_ig.vs['osmid'] = list(nx.get_node_attributes(graph, 'osmid').values())
    G_ig.es['length'] = list(nx.get_edge_attributes(graph, 'length').values())
    # print(G_ig.summary())

    path_lengths = np.array(G_ig.shortest_paths(source=origin,  weights='length'))
    path_lengths = path_lengths[:, ~np.isinf(path_lengths).any(axis=0)]

    mean = path_lengths.mean()
    std = path_lengths.std()
    return mean, std


def compute_area_m(nodes):
    return nodes.unary_union.convex_hull.area


def compute_center(nodes):
    bbox = box(*nodes.unary_union.bounds)

    return bbox.centroid


