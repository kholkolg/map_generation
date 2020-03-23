import pickle
import os
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.collections import LineCollection


def prepare_output(vertex_list):

    # print(node_map)
    edges = []
    for i in range(len(vertex_list)):
        vertex_list[i].id = i
    for v in vertex_list:
        for u in v.neighbours:
            edges.append([v.coords, u.coords])

    return edges


def save_vertexlist(vertex_list, name="output", savefig=1):
    print("Output is being saved. Number of vertices=", len(vertex_list))



    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    # print(path)
    edges = prepare_output(vertex_list)

    try:
        # print(path + "/temp/" + name, "wb")
        with open(path+"/temp/"+name, "wb") as f:
            pickle.dump(edges, f)
    except IOError as error:
        print("Specified output file doesn't exist: {0}".format(error))
        return 1


    print("Figure is being saved as " + name + ".png")

    lc = LineCollection(edges, linewidths=0.5, colors='black')
    fig, ax = plt.subplots()
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)
    plt.text(0, ax.get_ylim()[0], str(len(vertex_list)), fontsize=14)
    plt.savefig(path+"/outputs/"+name+".eps")
    print("New File " + name + " created in procedural_city_generation/temp/ with ", len(vertex_list), " vertices ")

    return 0





