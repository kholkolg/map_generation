import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import networkx as nx
import osmnx as ox
import geopandas as gpd
import os
from shapely.geometry import Point
from statistics.graph_metrics import *
import pandas as pd


def plot_network(edges, name):

     lc = LineCollection(edges, linewidths=0.5, colors='black')
     fig, ax = plt.subplots()
     ax.add_collection(lc)
     ax.autoscale()
     ax.margins(0.1)
     # path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
     # print(path)
     # plt.show()
     plt.savefig(name+".png")


def gre(grid_len, grid_height, cell_len, cell_height, p, q):

    cols = int(grid_len/cell_len)
    rows = int(grid_height/cell_height)
    # keep border edges, iterate left to right,bottom  to  top:
    #  - remove horizontal  edge with prob (1−p)
    #  - remove vertical edge e(i,0)(i,1) with the probab p(1−p)
    #  - remove a vertical edge e(i,j)(i,j+1) with probability (1−p) if exists e(i,j)(i+1,j)
    # For each vertex where both i and j are odd, generate diagonal edges with the probability q.
    edges = []
    edges.extend([((i, 0), (i+1, 0)) for i in range(rows)])
    edges.extend([((i, cols), (i+1, cols)) for i in range(rows)])
    # vertical borders
    edges.extend([((0, i), (0, i+1)) for i in range(cols)])
    edges.extend([((rows, i), (rows, i+1)) for i in range(cols)])
    #
    # plot_network(edges)
    edges = set(edges)

    for i in range(1, rows):
        for j in range(1, cols):
            # horizontal edges
            if np.random.uniform() > p:
                edges.add(((i, j), (i+1, j)))

            # vertical edges
            if j == 0 and np.random.uniform() > p*(1-p):
                edges.add(((i, j), (i, j+1)))

            if j > 0 and not ((i, j), (i+1)) in edges and np.random.uniform() > p:
                edges.add(((i, j), (i, j+1)))

            # diagonals
            if np.random.uniform() > q:
                edges.add(((i, j), (i+1, j+1)))
            if np.random.uniform() > q:
                 edges.add(((i, j), (i-1, j-1)))
            if np.random.uniform() > q:
                edges.add(((i, j), (i-1, j+1)))
            if np.random.uniform() > q:
                edges.add(((i, j), (i+1, j-1)))

    # plot_network(edges)
    return list(edges)


def edge_length(edge):
    return np.sqrt(((edge[0][0] - edge[1][0])**2 + (edge[0][1] - edge[1][1])**2))


def edgelist_to_graph(edge_list):
    nodes = list(set([n for e in edge_list for n in e]))
    key_map = {nodes[i]:i for i in range(len(nodes))}
    node_list = [(k, {'x':n[0], 'y':n[1]}) for n, k in key_map.items()]

    f = lambda e: (key_map[e[0]], key_map[e[1]], {'length': edge_length(e)})
    new_list = map(f, edge_list)
    G = nx.MultiDiGraph()
    G.add_nodes_from(node_list)
    G.add_edges_from(new_list)
    print(G.number_of_nodes(), G.number_of_edges())
    return G





if __name__ == '__main__':
    # edge_list = gre(5, 5, 0.2, 0.3, 0.35, 0.56)
    # G = nx.MultiDiGraph()
    # G.add_edges_from(edge_list)
    # print(len(G.nodes))
    results = []

    for i in range(2,7):
        for j in range(4,10):
            filename = 'grid_%s_%s'%(i,j)
            a = 0.1*i
            b = 0.1*j
            edge_list = gre(5, 5, 0.2, 0.3, 0.6, 0.6)
            result = {'p':0.6, 'q':0.6}
            plot_network(edge_list, filename)
            G = edgelist_to_graph(edge_list)
            result.update(edge_length_stats(G))
            result.update(degree_stats(G))
            nodes, data = zip(*G.nodes(data=True))
            gdf_nodes = gpd.GeoDataFrame(list(data), index=nodes)
            gdf_nodes['geometry'] = gdf_nodes.apply(lambda row: Point(row['x'], row['y']), axis=1)
            gdf_nodes.set_geometry('geometry', inplace=True)

            area = compute_area_m(gdf_nodes)
            result['area_km'] = area/10e6
            result['num_nodes'] = G.number_of_nodes()
            result['num_edges'] = G.number_of_edges()
            origin = compute_center(gdf_nodes)
            # print('origin ', origin)
            node0 = ox.get_nearest_node(G, (origin.y, origin.x),
                                        method='euclidean', return_dist=False)
            # print('node0 ', node0)
            central_paths = compute_paths(G, node0)
            result['central_sp_mean'] = central_paths[0]
            result['central_sp_std'] = central_paths[1]

            results.append(result)

    df = pd.DataFrame(results)
    print(df.head(5))
    df.to_csv('grids2.csv', index=False)

    # for k, v in result.items():
            #     print(k, ' - ', v)
