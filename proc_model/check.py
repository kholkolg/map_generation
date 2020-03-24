# -*- coding: utf-8 -*-
from __future__ import division
from proc_model.Vertex import Vertex

import numpy as np
from scipy.spatial import cKDTree
from proc_model.additional_stuff.Singleton import Singleton

singleton=Singleton("roadmap")


def check(suggested_vertex, neighbour, newfront):
    """
    Performs the following checks on a suggestes vertex and the suggested
    connection between this vertex and his last neighbour:

    1) Is the vertex out of bounds
        If yes, don't add this Vertex
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
    and the newfront, and return the newfront. This is the only place
    aftert config, where Vertices get added to the Global Lists.
    Every time a vertex is added, the cKDTree has to be updated too.

    Parameters
    ----------
    suggested_vertex : Vertex object
    neighbour : Vertex object
    newfront : list<Vertex>

    Returns
    -------
    newfront : list<Vertex>
    """
    #Checks if Neighbor is in Bounds
    # print('Check ', suggested_vertex, neighbour)

    # check if coordinates are not nans
    if not np.isfinite(suggested_vertex[0]) or not np.isfinite(suggested_vertex[1]):
        return newfront

    # 1 check borders
    if (abs(suggested_vertex[0]) > singleton.border[0] - singleton.maxLength) \
            or (abs(suggested_vertex[1]) > singleton.border[1] - singleton.maxLength):
        # print('out of bounds')
        return newfront

    #Finds all nearby Vertex and their distances
    distances, nearvertex = singleton.global_lists.tree.query(suggested_vertex.coords, 10,
                                                            distance_upper_bound=singleton.maxLength)
    print('nearvertex ', nearvertex)
    l = len(singleton.global_lists.vertex_list)
    nearvertex = [singleton.global_lists.vertex_list[x] for x in nearvertex if x < l]
    # print('nearvertex ', nearvertex)

    #Distances[0] is the distance to the nearest Vertex, nearve:
    #TODO probs
    if distances[0] < singleton.min_distance:

        #If the nearest Vertex is not a neighbor
        if nearvertex[0] not in neighbour.neighbours:

            #Find the best solution - as in the closest intersection
            bestsol = np.inf
            solvertex = None

            for k in nearvertex:
                for n in k.neighbours:
                    if n in nearvertex: #and not in doneliste
                        sol = get_intersection(neighbour.coords, nearvertex[0].coords-neighbour.coords, k.coords, n.coords-k.coords)
                        if np.isfinite(sol[0]) and np.isfinite(sol[1]) and sol[0] < bestsol:
                            bestsol = sol[0]
                            solvertex = [n, k]
            # If there is at least one solution, intersect that solution
            # See docstring #3 and #4
            if solvertex is not None:
                solvertex[1].neighbours.remove(solvertex[0])
                solvertex[0].neighbours.remove(solvertex[1])
                newk=Vertex(neighbour.coords + bestsol*(nearvertex[0].coords-neighbour.coords))
                singleton.global_lists.vertex_list.append(newk)
                singleton.global_lists.coordslist.append(newk.coords)
                singleton.global_lists.tree = cKDTree(singleton.global_lists.coordslist, leafsize=160)
                neighbour.connect(newk)
                solvertex[1].connect(newk)
                solvertex[0].connect(newk)
                return newfront
            else:
                #If there is no solution, the Vertex is clear
                #See docstring finish
                # print('else ', nearvertex[0], neighbour)
                nearvertex[0].connect(neighbour)
        return newfront

    bestsol = np.inf
    solvertex = None

    #If there is not an existing vertex too close, do the same thing but with
    # The vector between the suggested vertex and its neighbor
    for k in nearvertex:
        for n in k.neighbours:
            if n in nearvertex: #and not in doneliste
                sol = get_intersection(neighbour.coords, suggested_vertex.coords-neighbour.coords, k.coords, n.coords-k.coords)
                if np.isfinite(sol[0]) and np.isfinite(sol[1]) and sol[0] < bestsol:
                    bestsol = sol[0]
                    solvertex = [n, k]

    if solvertex is not None:
        solvertex[1].neighbours.remove(solvertex[0])
        solvertex[0].neighbours.remove(solvertex[1])

        newk=Vertex(neighbour.coords + bestsol*(suggested_vertex.coords-neighbour.coords))
        singleton.global_lists.vertex_list.append(newk)
        singleton.global_lists.coordslist.append(newk.coords)
        singleton.global_lists.tree = cKDTree(singleton.global_lists.coordslist, leafsize=160)
        neighbour.connect(newk)
        solvertex[1].connect(newk)
        solvertex[0].connect(newk)
        return newfront

    #If the Vertex is clear to go, add him and return newfront.

    suggested_vertex.connect(neighbour)
    newfront.append(suggested_vertex)
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
