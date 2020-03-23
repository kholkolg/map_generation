import geopandas as gpd
import numpy as np
import networkx as nx
import osmnx
from matplotlib import pyplot as plt
import igraph as ig
from shapely.geometry import box, Point
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


def compute_statisitcs(G, plot=False):

    result = edge_length_stats(G)
    result.update(degree_stats(G))
    nodes, data = zip(*G.nodes(data=True))
    gdf_nodes = gpd.GeoDataFrame(list(data), index=nodes)
    gdf_nodes['geometry'] = gdf_nodes.apply(lambda row: Point(row['x'], row['y']), axis=1)
    gdf_nodes.set_geometry('geometry', inplace=True)

    area = compute_area_m(gdf_nodes)
    result['area_km'] = area / 1e6
    result['num_nodes'] = G.number_of_nodes()
    result['num_edges'] = G.number_of_edges()
    result['node_density_km'] = result['num_nodes'] / result['area_km']
    result['edge_length_total'] = result['edge_length_avg']*result['num_edges']
    result['edge_density_km'] = result['edge_length_total'] / result['area_km']
    origin = compute_center(gdf_nodes)
    # print('origin ', origin)
    node0 = ox.get_nearest_node(G, (origin.y, origin.x),
                                method='euclidean', return_dist=False)
    # print('node0 ', node0)
    central_paths = compute_paths(G, node0)
    result['central_sp_mean'] = central_paths[0]
    result['central_sp_std'] = central_paths[1]
    result['degree_avg'] = result['in_degree_avg'] + result['out_degree_avg']
    result['degree_std'] = result['in_degree_std'] + result['out_degree_std']

    return result