import numpy as np
import random

from proc_model.Vertex import Vertex
from proc_model.additional_stuff.rotate import rotate

from proc_model.additional_stuff.Singleton import Singleton

singleton=Singleton("roadmap")
pSeed = singleton.pSeed
lMin = singleton.seedlMin
lMax = singleton.seedlMax


def seed(vertex, density):

    suggested_vertices = []


    l = len(vertex.neighbours)
    v1 = rotate(90, vertex.neighbours[0].coords - vertex.coords)
    v1_norm = np.linalg.norm(v1)
    if v1_norm <= 0.001:
        # print(v1_norm)
        return suggested_vertices

    if l == 1:
        v2 = v1
    elif l == 2:
        v2 = -rotate(90, vertex.neighbours[1].coords - vertex.coords)
    else:
        return suggested_vertices
    v2_norm = np.linalg.norm(v2)
    if v2_norm <= 0.001:
        return suggested_vertices

    v1 = v1/v1_norm
    v2 = v2/v2_norm

    #Rechts
    # print('pseed x dens ', pSeed * density)
    if density*pSeed > np.random.randint(0, 100):

        l1 = np.random.normal(lMin, lMax)
        k = np.random.uniform(0, 1)
        coords = ((1-k)*v1+k*v2)*l1
        k = Vertex(vertex.coords+coords)
        k.minor_road = True
        suggested_vertices.append(k)

    v1 = -v1
    v2 = -v2

    #Links
    # add counter to check probs
    # print('pseed x dens ', pSeed * density)
    if  density*pSeed > np.random.randint(0, 100):

        length = np.random.uniform(lMin, lMax)
        k=np.random.uniform(0, 1)

        coords = ((1-k)*v1+k*v2)*length
        k = Vertex(vertex.coords+coords)
        k.minor_road = True
        suggested_vertices.append(k)

    return suggested_vertices


def make_vertex(vertex, v1, v2):
    length = np.random.uniform(lMin, lMax)
    alpha = np.random.uniform(0, 1)

    coords = ((1 - alpha) * v1 + alpha * v2) * length
    vertex = Vertex(vertex.coords + coords)
    vertex.minor_road = True
    return vertex