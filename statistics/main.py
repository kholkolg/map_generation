import pandas as pd
import osmnx as ox
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
import scipy.spatial
from networkx import path_graph
from shapely.geometry import box, Point
import igraph as ig



BASIC_COLS = ['n', 'm', 'k_avg', 'edge_length_total', 'edge_length_avg',
              'node_density_km', 'edge_density_km', 'city', 'area_km']


def edge_length_stats(graph):

    lengths = np.array([x['length'] for _, x in graph.edges.items() if x['length'] > 10])
    # lengths.sort()
    mean = lengths.mean()
    sigma = lengths.std()
    # n = len(lengths)
    # lens = np.array(lengths)

    return {'edge_length_avg10':mean, 'edge_length_std10':sigma}


def degree_stats(graph):

    in_degrees = np.array([d for e, d in graph.in_degree])
    in_mean = in_degrees.mean()
    in_sigma = in_degrees.std()

    out_degrees = np.array([d for e, d in graph.out_degree])
    out_mean = out_degrees.mean()
    out_sigma = out_degrees.std()

    return {'in_degree_avg':in_mean, 'in_degree_std':in_sigma,
            'out_degree_avg':out_mean, 'out_degree_std':out_sigma}


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
        G = nx.relabel.convert_node_labels_to_integers(G)
    except Exception as ex:
        print(place, '1: ', ex)
        try:
            G = ox.graph_from_place(place, which_result=2, network_type='drive')
            G = nx.relabel.convert_node_labels_to_integers(G)
        except Exception as ex:
            print(place, '2: ', ex)
    return G


def city_statistics(city:str):

    result = {'city': city}
    G = get_graph(city)
    if G is None:
        return result

    G_proj = ox.project_graph(G)
    nodes_proj = ox.graph_to_gdfs(G_proj, edges=False)
    nodes_uu = nodes_proj.unary_union

    area = nodes_uu.convex_hull.area
    result['area_km'] = area/10e6
    bs = compute_basic_stats(G, area)
    #basic statistics from osmnx
    result.update(bs)

    result.update(edge_length_stats(G))
    result.update(degree_stats(G))

    bbox = box(*nodes_uu.bounds)
    orig_point = bbox.centroid
    node0 = ox.get_nearest_node(G_proj, (orig_point.y, orig_point.x),
                                method='euclidean', return_dist=False)
    # print('node0 ', node0)
    central_paths = compute_paths(G_proj, node0)
    result['central_sp_mean'] = central_paths[0]
    result['central_sp_std'] = central_paths[1]
    result.update(compute_extended_stats(G))
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
    path_lengths = np.array(G_ig.shortest_paths(source=origin,  weights='length'))
    # paths = nx.shortest_path(G=graph, source=origin, weight='length')
    path_lengths = path_lengths[:,~np.isinf(path_lengths).any(axis=0)]
    # print(path_lengths[0])
    # plt.hist(path_lengths[0], 50, density=True)
    # plt.show()

    mean = path_lengths.mean()
    std = path_lengths.std()
    return mean, std

# def compute_dist(graph, origin):
#     xa = np.array([[graph.nodes[origin]['x'], graph.nodes[origin]['y']]])
#     xb = np.array([v for v in map(lambda n: [n['x'], n['y']], graph.nodes.values())])
#
#     dist = scipy.spatial.distance.cdist(xa, xb)[0]
#     print(dist)
#     df = pd.DataFrame({'sp_dist':path_lengths, 'eucl_dist':dist})
#     print(df.head(5))
#    # df['ratio'] = df['sp_dist']/df['eucl_dist']
#     print(df.head(20))
#     return dist


def prepare_stats(cities, filename):
    results = []
    for c in cities:
        print(c)
        results.append(city_statistics(c))

    # print(results)
    df = pd.DataFrame(results)
    print(df.head(5))
    df.to_csv(filename, index=False)









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
                   'Shanghai', 'Beijing', 'Chongqing',
                   'Mumbai', 'Delhi', 'Bangalore',
                   'Bangkok', 'Singapore']
    all = {'europe': cities_eu, 'us': cities_us, }

    # ox.config(use_cache=True)

    # for name, cities in all.items():
    #     prepare_stats(cities, name + '.csv')

    df =  pd.read_csv('graph_statistics2.csv', index_col=None)
    print(df.columns)
    df.drop(columns=['edge_length_avg_y'], inplace=True)
    df.rename(columns={'n':'num_nodes','m':'num_edges',
                       'edge_length_avg_x':'edge_length_avg',
                       'k_avg':'degree_avg'}, inplace=True)
    df['degree_std'] = df['in_degree_std']+df['out_degree_std']
    df.to_csv('graphs1.csv', index=False)
    df.drop(columns=['in_degree_avg', 'in_degree_std', 'out_degree_avg', 'out_degree_std'], inplace=True)
    df.to_csv('graph_statistics.csv', index=False)
    print(df.columns)
    print(df.head(5))

    # df1 = pd.read_csv('europe.csv', index_col=None)
    # df2 = pd.read_csv('us.csv', index_col=None)
    # print(df1.info, df2.info)
    # df_basic = pd.concat([df1, df2], axis=0)
    # df_basic.drop(columns=['Unnamed: 0'], inplace=True)
    # print(df_basic.head(5))
    #
    # df1 = pd.read_csv('europe_sp.csv', index_col=None)
    # df2 = pd.read_csv('us_sp.csv', index_col=None)
    # df_sp = pd.concat([df1, df2], axis=0)
    # df_sp.drop(columns=['Unnamed: 0'], inplace=True)
    # print(df_sp.head(5))
    #
    # df = pd.merge(df_basic, df_sp, on='city')
    # df.dropna(axis=0, inplace=True)
    # print(df.head(5))
    # df.to_csv('graph_statistics.csv', index=False)
    # df = df[df['n'] >= 8000]

    df = pd.read_csv('graph_statistics.csv', index_col=None)
    for col in df.columns:
        if col == 'city': continue
        ax = df.hist(column=col, bins=10)
        plt.show()
