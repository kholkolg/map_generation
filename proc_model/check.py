# -*- coding: utf-8 -*-

from proc_model.Vertex import Vertex

import numpy as np
from scipy.spatial import cKDTree
from proc_model.additional_stuff.Singleton import Singleton
singleton=Singleton("roadmap")

# What the hell is that thing doing?
EPS = 1e5
def is_valid(sol):
    return EPS < sol[0] < (1-EPS) and EPS < sol[1] < (1-EPS)


def check(suggested_vertex, neighbour, newfront):
    """
    Performs the following checks on a suggestes vertex and the suggested
    connection between this vertex and his last neighbour:

    1) Is the vertex out of bounds
        If yes, dont add this Vertex
    2) Is the vertex too close to an existing vertex
        If yes, change the vector that is checked in 4 and 5 from
        [neighbor-suggested_vertex] to [neighbor-closest_existing_point]
    3) Does the the vector intersect an existing connection (road)
        If yes, only create the connection up until that intersection.
        Add that intersection to the Global_lists and fix the neighbor
        attribute of the existing connection that was "intersected".
    4) Does the vector stop shortly before an existing connection
        If yes, extend the connection up until that intersection.
        Add that intersection to the Global_lists and fix the neighbor
        attribute of the existing connection that was "intersected".
    If none of the above, simply add this vertex to the global_lists
    and the new front and return the newfront. This is the only place
    aftert config, where Vertices get added to the Global Lists. Every Time
    A vertex is added, the cKDTree used to find the closest vertices has to
    be updated.

    Parameters
    ----------
    suggested_vertex : Vertex object
    neighbour : Vertex object
    newfront : list<Vertex>

    Returns
    -------
    newfront : list<Vertex>
    """


    # print('Check ', suggested_vertex, neighbour)
    if not np.isfinite(suggested_vertex[0]) or not np.isfinite(suggested_vertex[1]):
        return newfront

    #Checks if suggested vertex is inside the bounds
    if (abs(suggested_vertex.coords[0]) > singleton.border[0]-singleton.maxLength) \
            or (abs(suggested_vertex.coords[1]) > singleton.border[1]-singleton.maxLength):
        # print('out of bounds')
        return newfront

    #Finds 10 nearest vertices and their distances
    distances, nearvertex = singleton.global_lists.tree.query(suggested_vertex.coords, 10,
                                                            distance_upper_bound=singleton.maxLength)

    # vertices in kdtree have same indices as in global list
    max_index = len(singleton.global_lists.vertex_list)
    nearvertex = [singleton.global_lists.vertex_list[i] for i in nearvertex if i < max_index]

    # Find the best solution - as in the closest intersection
    bestsol, solvertex = find_best_solution(neighbour, nearvertex)

    if solvertex is not None:
        reconnect(suggested_vertex, neighbour, bestsol, solvertex)
        return newfront


    #Distances[0] is the distance to the nearest vertex:
    if distances[0] < singleton.min_distance:
        #If the nearest vertex is not a neighbor
        if nearvertex[0] not in neighbour.neighbours:
            nearvertex[0].connect(neighbour)
        return newfront


    #If the Vertex is clear to go, add him and return newfront.
    suggested_vertex.connect(neighbour)
    newfront.append(suggested_vertex)
    #FIXME refactor
    singleton.global_lists.vertex_list.append(suggested_vertex)
    singleton.global_lists.coordslist.append(suggested_vertex.coords)
    singleton.global_lists.tree = cKDTree(singleton.global_lists.coordslist, leafsize=160)
    return newfront


def get_intersection(a, ab, c, cd):
    """Gets the intersection coordinates between two lines.
    If it does not exist (lines are parrallel), returns np.array([np.inf, np.inf])

    Parameters
    ----------
    a : np.ndarray(2, 1)
        Starting point of first vector
    ab : np.ndarray(2, 1)
        First vector (b-a)
    c : np.ndarray(2, 1)
        Starting point of second vector
    cd : np.ndarray(2, 1)
        Second vector (d-c)

    Returns
    -------
    intersection : np.ndarray(2, 1)
    """
    try:
        return np.linalg.solve(np.array([ab, -cd]).T, c-a)
    except np.linalg.linalg.LinAlgError:
        return np.array([np.inf, np.inf])


def find_best_solution(neighbour, nearvertex):
    # Find the best solution - as in the closest intersection
    bestsol = np.inf
    solvertex = None

    for k in nearvertex:
        for n in k.neighbours:
            if n in nearvertex:  # and not in doneliste
                sol = get_intersection(neighbour.coords, nearvertex[0].coords - neighbour.coords, k.coords,
                                       n.coords - k.coords)
                if is_valid(sol) and sol[0] < bestsol:
                    bestsol = sol[0]
                    solvertex = [n, k]

    return bestsol, solvertex


def reconnect(suggested_vertex, neighbour, bestsol, solvertex):

    solvertex[1].neighbours.remove(solvertex[0])
    solvertex[0].neighbours.remove(solvertex[1])

    newk = Vertex(neighbour.coords + bestsol * (suggested_vertex.coords - neighbour.coords))
    #TODO add method to global lists
    singleton.global_lists.vertex_list.append(newk)
    singleton.global_lists.coordslist.append(newk.coords)
    singleton.global_lists.tree = cKDTree(singleton.global_lists.coordslist, leafsize=160)
    neighbour.connect(newk)
    solvertex[1].connect(newk)
    solvertex[0].connect(newk)

