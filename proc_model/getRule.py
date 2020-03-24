# -*- coding: utf-8 -*-

import numpy as np
from proc_model.additional_stuff.Singleton import Singleton

singleton=Singleton("roadmap")

def getRule(vertex):
    """
    Gets the correct growth_rule for a Vertex, depending on that objects'
    xy coordinates and the growth_rule_image

    Parameters
    ----------
    vertex : Vertex object

    Returns
    -------
    tuple(int, np.ndarray(3, ) , float)
        (int) for choosing the correct growth rule,
        (np.ndarray) for center in case that the radial rule is chosen,
        (float) for population_density
    """

    # print('rule ', vertex)
    #

    x = (vertex.coords[0]+singleton.border[0])/(singleton.border[0]*2)
    y = (vertex.coords[1]+singleton.border[1])/(singleton.border[1]*2)
    # print('x=',x,', y=',y)

    x_, y_ = 0, 0
    try:
        x_ = int(singleton.img2.shape[0]*(1-y))
    except ValueError as err:
        print(vertex, err)
    try:
        y_ = int(singleton.img2.shape[1]*x)
    except ValueError as err:
        print(vertex, err)

    # s2 = s0*(1-y)
    # print(s2, singleton.img2.shape[0]-y*singleton.img2.shape[0])
    # print(singleton.img2[s2])
    # im = singleton.img2[x_][y_][0]
    population_density = np.sqrt((singleton.img2[x_][y_][0]))
    # print('density ', population_density)

    if vertex.seed:
        return (4, None, population_density)


    if not vertex.minor_road:
        #Finds the relative position of the vertex on the growth_rule_image
        intrule=np.argmax(singleton.img[int(singleton.img.shape[0]-y*singleton.img.shape[0])][int(x*singleton.img.shape[1])])
        z=(0, 0)

        #If the rule is radial, find the closest radial center
        if intrule == 2:
            z=singleton.center[np.argmin(np.linalg.norm(vertex.coords-singleton.center, axis=1))]
        return (intrule, z, population_density)
    else:
        return (3, None, population_density)
