
import numpy as np
import random
from proc_model.Vertex import Vertex
from proc_model.additional_stuff.rotate import rotate
from proc_model.additional_stuff.Singleton import Singleton


singleton=Singleton("roadmap")

def grid(vertex, b):

    #Sammelt Numerische Werte aus Variables-Objekt
    pForward = singleton.gridpForward
    pTurn = singleton.gridpTurn
    lMin = singleton.gridlMin
    lMax = singleton.gridlMax


    suggested_vertices=[]
    weiter=True


    #Berechnet den Vektor des letzten Weges zu diesem Punkt

    previous_vector=np.array(vertex.coords-vertex.neighbours[-1].coords)
    pv_norm = np.linalg.norm(previous_vector)
    if pv_norm <= 0.0001:
        return  suggested_vertices

    previous_vector=previous_vector/pv_norm
    # print('v-u ',len(vertex.neighbours), vertex, vertex.neighbours[-1])
    # print('previous vector ', previous_vector, np.linalg.norm(previous_vector))

    n=np.array([-previous_vector[1], previous_vector[0]])

    #Geradeaus

    v=random.uniform(lMin, lMax)*previous_vector
    # print('v ', v)
    random_number=random.randint(0, 100)
    if random_number<=pForward:
        k=Vertex(vertex.coords+v)

        suggested_vertices.append(k)
        weiter=False
    #Rechts
    # v=random.uniform(lMin, lMax)*previous_vector
    random_number=random.randint(0, 100)
    if random_number<=pTurn*b*b:
        k=Vertex(vertex.coords+n)

        suggested_vertices.append(k)
        weiter=True

    #Links
    # v=random.uniform(lMin, lMax)*previous_vector
    random_number=random.randint(0, 100)
    if random_number<=pTurn*b*b:
        k=Vertex(vertex.coords-n)

        suggested_vertices.append(k)
        weiter=True


    #Seed!
    if not weiter:
        vertex.seed=True
        singleton.global_lists.vertex_queue.append([vertex, 0])

    return suggested_vertices

