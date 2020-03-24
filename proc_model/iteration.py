# -*- coding: utf-8 -*-

import numpy as np
from proc_model.getSuggestion import getSuggestion
from proc_model.check import check
from proc_model.additional_stuff.Singleton import Singleton

singleton=Singleton("roadmap")

def iteration(front):
    """
    Gets Called in the mainloop.
    Manages the front and newfront and the queue

    Parameters
    ----------
    front : list<Vertex>

    Returns
    -------
    newfront : list<Vertex>

    """
    newfront=[]


    for vertex in front:
        # print('iter ', vertex)
        if vertex.id == 'nan-nan':
            print('Nan ', vertex)
            continue
        # if len(vertex.neighbours) >= singleton.degree:
        #     print('degree')
        #     return newfront
        for suggested_vertex in getSuggestion(vertex):
            # if suggested_vertex[0] == np.nan or suggested_vertex[0] == np.nan:
            #     print("suggested vertex NAN: ", suggested_vertex)
            #     continue
            newfront=check(suggested_vertex, vertex, newfront)

    #Increments index of each element in queue
    singleton.global_lists.vertex_queue=[[x[0], x[1]+1] for x in singleton.global_lists.vertex_queue]

    #Finds elements in queue which are to be added into the newfront
    while singleton.global_lists.vertex_queue!=[] and singleton.global_lists.vertex_queue[0][1]>=singleton.minor_road_delay:
        newfront.append(singleton.global_lists.vertex_queue.pop(0)[0])
    # print('newfront size ', len(newfront))
    return newfront
