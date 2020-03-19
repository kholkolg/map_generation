import pandas as pd
import osmnx as ox
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
import scipy.spatial
from networkx import path_graph
from shapely.geometry import box, Point
import igraph as ig
import operator


BASIC_COLS = ['n', 'm', 'k_avg', 'edge_length_total', 'edge_length_avg',
              'node_density_km', 'edge_density_km', 'city', 'area_km']


def compute_graph_area(graph):

    nodes_proj = ox.graph_to_gdfs(graph, edges=False)

    bbox = box(*nodes_proj.unary_union.bounds)
    orig_point = bbox.centroid
    print(orig_point)
    node0 = ox.get_nearest_node(graph, orig_point, method='euclidean', return_dist=False)
    print(node0)
    graph_area = nodes_proj.unary_union.convex_hull.area
    return graph_area


def compute_basic_stats(graph, area):
    data = ox.basic_stats(graph, area=area)
    return {k: v for k, v in data.items() if k in BASIC_COLS}


def compute_extended_stats(graph):
    data = ox.extended_stats(graph, connectivity=True, cc=True, ecc=True, bc=True)
    return {k: v for k, v in data.items() if isinstance(v, float) or isinstance(v, int)}


def get_graph(place:str):

    G = None
    try:
        G = ox.graph_from_place(place, network_type='drive')
    except Exception as ex:
        print(place, '1: ', ex)
        try:
            G = ox.graph_from_place(place, which_result=2, network_type='drive')
        except Exception as ex:
            print(place, '2: ', ex)

    G = nx.relabel.convert_node_labels_to_integers(G)
    return G


def city_statistics(city:str):

    result = {'city': city}
    G = get_graph(city)
    if G is None:
        return result

    G_proj = ox.project_graph(G)
    nodes_proj = ox.graph_to_gdfs(G_proj, edges=False)
    nodes_uu = nodes_proj.unary_union

    bbox = box(*nodes_uu.bounds)
    orig_point: Point = bbox.centroid
    print('origin ', orig_point)

    node0 = ox.get_nearest_node(G_proj, (orig_point.y, orig_point.x),
                                method='euclidean', return_dist=False)
    print('node0 ', node0)

    area = nodes_uu.convex_hull.area

    # area = compute_graph_area(G)
    result['area_km'] = area/10e6

    bs = compute_basic_stats(G, area)
    result.update(bs)

    compute_paths(G_proj, node0)
    # result.update(compute_extended_stats(G))
    # print(result)
    return result


def compute_paths(graph, origin):
    # print(origin, type(origin))
    # convert networkx graph to igraph
    G_ig = ig.Graph(directed=True)

    G_ig.add_vertices(list(graph.nodes()))
    G_ig.add_edges(list(graph.edges()))

    # G_ig.vs['osmid'] = list(nx.get_node_attributes(graph, 'osmid').values())
    G_ig.es['length'] = list(nx.get_edge_attributes(graph, 'length').values())
    # print(G_ig.summary())

    # for n,d in graph.nodes.items():
    #     print(n,d)
    path_lengths = G_ig.shortest_paths(source=origin,  weights='length')[0]
    # paths = nx.shortest_path(G=graph, source=origin, weight='length')
    path_lengths = path_lengths[~np.isinf(path_lengths).any(axis=1)]
    print(path_lengths)
    plt.hist(path_lengths, 100)
    plt.show()
    # xa = np.array([[graph.nodes[origin]['x'], graph.nodes[origin]['y']]])
    # xb = np.array([v for v in map(lambda n: [n['x'], n['y']], graph.nodes.values())])

    # edist = scipy.spatial.distance.cdist(xa, xb)[0]
    # print(edist)
    # df = pd.DataFrame({'sp_dist':path_lengths, 'eucl_dist':edist})
    # print(df.head(5))
    # df['ratio'] = df['sp_dist']/df['eucl_dist']
    # print(df.head(20))
    return path_lengths



def prepare_stats(cities, filename):
    results = []
    for c in cities:
        print(c)
        # G = ox.graph_from_place(c, network_type='drive', simplify=True)
        # ox.plot_graph(G)

        # df = ox.gdf_from_place(c, which_result=2)
        # print(df.head(5))

        results.append(city_statistics(c))

    print(results)
    df = pd.DataFrame(results)
    print(df.head(5))
    # columns = ['n', 'm', 'k_avg', 'edge_length_total', 'edge_length_avg',
    #                'node_density_km', 'edge_density_km', 'city', 'area_m2']
    # df.drop(columns=[c for c in df.columns if c not in columns], inplace=True)
    df.to_csv(filename)
    print(df.head(5))








if __name__ == '__main__':

    cities_eu = ['Prague', 'Paris', 'London', 'Berlin', 'Madrid', 'Brussels', 'Stockholm',
                 'Helsinki', 'Oslo', 'Warsaw', 'Vienna', 'Amsterdam', 'Antwerp, Netherlands',
                 'Athens, Greece', 'Barcelona', 'Belgrade', 'Bilbao', 'Birmingham', 'Bremen', 'Bristol',
                 'Copenhagen', 'Dublin', 'Glasgow', 'Hamburg', 'Liverpool', 'Lisbon',
                 'Manchester', 'Milan', 'Munich', 'Naples', 'Rome', 'Rotterdam']

    cities_us = ['New York, New York', 'San Francisco, California', 'Los Angeles, California',
                 'Boston, Massachusetts', 'Washington, DC', 'Seattle, Washington', 'San Diego, Texas',
                 'Chicago, Illinois', 'Houston, Texas', 'Philadelphia, Philadelphia', 'Phoenix, Arizona',
                 'Dallas, Texas', 'Detroit, Michigan', 'Memphis, Tennessee']

    cities_asia = ['Tokyo', 'Yokohama', 'Osaka',
                   'Shanghai, China', 'Beijing, China', 'Chongqing, China',
                   'Mumbai, India', 'Delhi, India', 'Bangalore, India',
                   'Bangkok, Thailand', 'Singapore']

    all = {'europe': cities_eu, 'us': cities_us, 'asia': cities_asia}

    # for name, cities in all.items():
    # prepare_stats(cities_asia, 'asia_basic.csv')

    ox.config(use_cache=True, log_console=True)
    city_statistics('Prague')