from __future__ import division
import numpy as np
import random

from proc_model.Vertex import Vertex
from proc_model.additional_stuff.rotate import rotate

from proc_model.additional_stuff.Singleton import Singleton

singleton=Singleton("roadmap")

def minor_road(vertex, b):

    #Sammelt Numerische Werte aus Variables-Objekt
    pForward = singleton.minor_roadpForward
    pTurn = singleton.minor_roadpTurn
    lMin = singleton.minor_roadlMin
    lMax = singleton.minor_roadlMax

    suggested_vertices=[]


    #Berechnet den Vektor des letzten Weges zu diesem Punkt

    previous_vector=np.array(vertex.coords-vertex.neighbours[-1].coords)
    pv_norm = np.linalg.norm(previous_vector)
    if pv_norm <= 0.0001:
        return suggested_vertices

    previous_vector = previous_vector / pv_norm

    n=np.array([-previous_vector[1], previous_vector[0]])

    #Geradeaus
    v = random.uniform(lMin, lMax) * previous_vector

    random_number = random.randint(0, 100)
    print('pForward*dens ',pForward*b )
    if random_number < pForward*b:
        k = Vertex(vertex.coords+v)
        #k.neighbours.append(vertex)
        k.minor_road = True
        suggested_vertices.append(k)

    #Rechts
    random_number = random.randint(0, 100)
    print('pForward*dens ', pForward * b)
    if random_number < pTurn*b:
        k = Vertex(vertex.coords+n)
        #k.neighbours.append(vertex)
        k.minor_road = True
        suggested_vertices.append(k)

    #Links
    random_number = random.randint(0, 100)
    if random_number < pTurn*b:
        k = Vertex(vertex.coords-n)
        #k.neighbours.append(vertex)
        k.minor_road = True
        suggested_vertices.append(k)

    return suggested_vertices
