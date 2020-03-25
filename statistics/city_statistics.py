import pandas as pd
import osmnx as ox
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
import scipy.spatial
from shapely.geometry import box, Point
from statistics.graph_metrics import *


BASIC_COLS = ['n', 'm', 'k_avg', 'edge_length_total', 'edge_length_avg',
              'node_density_km', 'edge_density_km', 'city', 'area_km']


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


def one_ways(graph):
    oneways = [data['length'] for  u,v, data in graph.edges( data=True) if data['oneway']]
    result = {'num_oneway':len(oneways), 'len_oneways':sum(oneways)}
    print(result)
    return result



def city_statistics(city:str):

    result = {'city': city}
    G = get_graph(city)
    if G is None:
        return result

    G_proj = ox.project_graph(G)
    nodes_proj = ox.graph_to_gdfs(G_proj, edges=False)

    result = one_ways(G_proj)

    # area = compute_area_m(nodes_proj)
    # result['area_km'] = area/1e6
    # bs = compute_basic_stats(G, area)
    # #basic statistics from osmnx
    # result.update(bs)
    #
    # result.update(edge_length_stats(G))
    # result.update(degree_stats(G))
    # result.update(one_ways(G_proj))
    # orig_point = compute_center(nodes_proj)
    # node0 = ox.get_nearest_node(G_proj, (orig_point.y, orig_point.x),
    #                             method='euclidean', return_dist=False)
    # # print('node0 ', node0)
    # central_paths = compute_paths(G_proj, node0)
    # result['central_sp_mean'] = central_paths[0]
    # result['central_sp_std'] = central_paths[1]
    # result.update(compute_extended_stats(G))
    # print(result)
    return result


def prepare_stats(cities, filename):
    results = []
    for c in cities:
        print(c)
        results.append(city_statistics(c))

    # print(results)
    df = pd.DataFrame(results)
    print(df.head(5))
    df.to_csv(filename, index=False)
    return df





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
    df = pd.DataFrame()
    for name, cities in all.items():
        df = pd.concat([df, prepare_stats(cities, name + '_1ways.csv')], axis=0)

    print(df.head(5))
    df1 = pd.read_csv('data\graph_statistics2.csv', index_col=None)
    print(df1.columns)
    df1.drop(columns=['Unnamed: 0'], inplace=True)
    df1['area_km'] = df1['area_km']*10
    print(df1.columns)

    df = pd.merge(df, df1, on='city')
    print(df.head(5))
    df.to_csv('data\graph_statistics_1w.csv', index=False)

    # df.rename(columns={'n':'num_nodes','m':'num_edges',
    #                    'edge_length_avg_x':'edge_length_avg',
    #                    'k_avg':'degree_avg'}, inplace=True)
    # df['degree_std'] = df['in_degree_std']+df['out_degree_std']
    # df.to_csv('graphs1.csv', index=False)
    # df.drop(columns=['in_degree_avg', 'in_degree_std', 'out_degree_avg', 'out_degree_std'], inplace=True)
    # df.to_csv('data\graph_statistics.csv', index=False)
    # print(df.columns)
    # print(df.head(5))

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

    # df = pd.read_csv('graph_statistics.csv', index_col=None)
    # for col in df.columns:
    #     if col == 'city': continue
    #     ax = df.hist(column=col, bins=10)
    #     plt.show()
