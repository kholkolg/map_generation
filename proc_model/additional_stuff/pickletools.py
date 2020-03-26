import pickle
import os
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.collections import LineCollection
from datetime import datetime

def prepare_output(vertex_list):

    # print(node_map)

    # node_map = {vertex_list[i].id: i for i in range(len(vertex_list))}
    edges = []
    for i in range(len(vertex_list)):
        vertex_list[i].id = i
    for v in vertex_list:
        # new_id = node_map[v.id]
        for u in v.neighbours:
            edges.append([v.coords, u.coords])
            # edges.append((new_id, node_map[u.id]))
    # print('number of edges ', len(edges))
    #
    # G = nx.DiGraph()
    # nodes = [(node_map[v.id], {'x': v[0], 'y': v[1]}) for v in vertex_list]
    # G.add_nodes_from(nodes)
    # G.add_edges_from(edges)
    # # nx.draw(G)
    return edges


def save_vertexlist(vertex_list, name, savefig=0):
    print("Output is being saved. Number of vertices=", len(vertex_list))



    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    # print(path)
    edges = prepare_output(vertex_list)

    # try:
    #     # print(path + "/temp/" + name, "wb")
    #     with open(path+"/temp/"+name, "wb") as f:
    #         pickle.dump(edges, f)
    # except IOError as error:
    #     print("Specified output file doesn't exist: {0}".format(error))
    #     return 1


    # for k in vertex_list:
    #     for n in k.neighbours:
    #         col = 'black'
    #         width = 1
    #         if n.minor_road or k.minor_road:
    #             col = 'blue'
    #             width = 0.5
    #
    #         plt.plot([n.coords[0], k.coords[0]], [n.coords[1], k.coords[1]],
    #                     color=col,linewidth=width)

    lc = LineCollection(edges, linewidths=0.5, colors='black')
    fig, ax = plt.subplots()
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)
    plt.text(0, ax.get_ylim()[0], str(len(vertex_list)), fontsize=14)
    timestamp = datetime.now().strftime("%H_%M_%S.%f")
    if savefig:
        print("Figure is being saved as " + name + timestamp + "_.png")
        plt.savefig(os.path.join(path, 'outputs', name + timestamp + ".png"))
    # print("New File " + name + " created in procedural_city_generation/temp/ with ", len(vertex_list), " vertices ")

    return 0




