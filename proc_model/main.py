#!/usr/bin/env python
# -*- coding: utf-8 -*-
from proc_model.additional_stuff.Singleton import Singleton
from proc_model.additional_stuff.pickletools import save_vertexlist
from proc_model.config import config
from proc_model.iteration import iteration
from copy import copy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from statistics.graph_metrics import compute_statisitcs
import os, sys
import random

random.seed(42)
np.random.seed(42)
singleton = Singleton("roadmap")


def generate_map():
    # print('proc_model.main')


    # print(singleton)

    front = copy(singleton.global_lists.vertex_list)
    print('1 ', front)
    front.pop(0)
    print('2 ',front)
    front.pop()
    print('3 ', front)

    # i=0
    while len(front) > 0 or len(singleton.global_lists.vertex_queue) > 0:
        # i+=1
        front=iteration(front)
        # print(i)

    print("Roadmap is complete ", singleton.output_name)
    # path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    # with open(path + "/output/" + singleton.output_name, "wb") as f:
    #     pickle.dump(singleton.global_lists.vertex_list, f)
    # save_vertexlist(singleton.global_lists.vertex_list, singleton.output_name )

    # print(singleton.global_lists.vertex_list)
    # if gui is None and singleton.plot == 1:
    #     if singleton.plot == 1:
    #         plt.show()
    return singleton.global_lists.vertex_list




def to_nx(vertex_list):

    nodes = [{'x': x, 'y':y} for x,y in vertex_list]
    # nodes = list(set([(v[0], v[1]) for v in vertex_list]))
    # nodes = [n for n in nodes if np.isfinite(n['x']) and np.isfinite(n['y'])]
    key_map = {(v['x'], v['y']): k for k, v in enumerate(nodes)}
    # print(key_map)

    edges = []
    for v in vertex_list:
        coords_v = tuple(v)
        if coords_v not in key_map.keys():
            print('not in list', coords_v)
            continue
        vid = key_map[coords_v]
        for u in v.neighbours:
            coords_u = tuple(u)
            if coords_u not in key_map:
                # print('not in list', coords_u)
                continue
            if coords_u == coords_v:
                # print('loop')
                continue
            length = np.sqrt((coords_v[0] - coords_u[0]) ** 2 + (coords_v[1] - coords_u[1]) ** 2)

            uid = key_map[coords_u]

            edges.append((vid, uid, {'length': length}))

    G = nx.MultiDiGraph()
    G.add_nodes_from(enumerate(nodes))
    G.add_edges_from(edges)

    draw_edges(G)

    #    pos : {node:[x, y]}
    # nx.draw_networkx_edges(G, pos={k :[v['x'], v['y']] for k, v in G.nodes(data=True)},
    #                        edge_color='black', arrowsize=10, node_size=10)
    # plt.show()

    return G


def draw_edges(G):
    print(G.number_of_nodes(), G.number_of_edges())
    lines = [[[G.nodes[u]['x'], G.nodes[u]['y']], [G.nodes[v]['x'], G.nodes[v]['y']]] for u, v, _ in G.edges]
    lc = LineCollection(lines, linewidths=0.5, colors='black')
    _, ax = plt.subplots()
    ax.add_collection(lc)
    ax.autoscale()
    plt.show()


def find_scc(graph):

    scc = max(nx.strongly_connected_components(graph), key=len)
    # print('scc ', scc)
    nodes = [(n[0], {'x': n[1]['x'], 'y': n[1]['y']}) for n in graph.nodes(data=True) if n and n[0] in scc]
    edges = [(u, v, d) for u, v, d in graph.edges(data=True) if (u in scc) and (v in scc)]
    # print(len(edges))

    graph_scc = nx.MultiDiGraph()
    graph_scc.add_nodes_from(nodes)
    graph_scc.add_edges_from(edges)
    graph_scc = nx.relabel.convert_node_labels_to_integers(graph_scc)
    draw_edges(graph_scc)
    print('New graph: ', graph_scc.number_of_nodes(), graph_scc.number_of_edges())
    # Gc = max(nx.strongly_connected_subgraphs(graph), key=len)
    return graph_scc

if __name__ == '__main__':

    import pandas as pd
    parentpath=os.path.join(os.getcwd(), ("../../"))
    sys.path.append(parentpath)

    results = []
    for i in range(1):

        singleton = config()
        # singleton.min_distance = i
        # singleton.output_name += str(i)
        print(singleton.min_distance)
        vlist = generate_map()

        graph = to_nx(vlist)
        graph = find_scc(graph)

        result = {'city': singleton.output_name + '_md%s' % singleton.min_distance}
        result.update(compute_statisitcs(graph))
        results.append(result)
        print(result)

        result_scc = {'city': singleton.output_name + 'scc_md%s' % singleton.min_distance}
        result_scc.update(compute_statisitcs(graph_scc))
        results.append(result_scc)
        print(result_scc)

    df = pd.DataFrame(results)
    df.drop(columns=['in_degree_avg', 'in_degree_std', 'out_degree_avg', 'out_degree_std'], inplace=True)
    print(df.head(5))
    path = os.path.join(singleton.path, 'outputs', singleton.output_name +'.csv')
    df.to_csv(path, index=False)


    # for k, v in result.items():
    #     print(k, v)
    # lengths = np.array([x['length'] for _, x in graph.edges.items()])
    # plt.hist(lengths, 50, density=True)
    # plt.show()
