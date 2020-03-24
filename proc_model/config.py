# -*- coding:utf-8 -*-

from proc_model.config_functions.input_image_setup import input_image_setup
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import proc_model
import os
from proc_model.Vertex import Vertex
from proc_model.additional_stuff.Singleton import Singleton
from proc_model.config_functions.find_radial_centers import find_radial_centers


class Global_Lists:
    def __init__(self):
        self.vertex_list=[]
        self.vertex_queue=[]
        self.tree=None

def config():
    """
    Starts the program up with all necessary things. Reads the inputs,
    creates the Singleton objects properly, sets up the heightmap for later,
    makes sure all Vertices in the axiom have the correct neighbor. Could
    need a rework in which the Singletons are unified and not broken as they
    are now.

    Returns
    -------
    variables : Variables object
        Singleton with all numeric values which are not to be changed at runtime
    singleton.global_lists : singleton.global_lists object
        Singleton with the Global Lists which will be altered at runtime
    """


    print('config')
    path=os.path.dirname(proc_model.__file__)

    singleton=Singleton("roadmap")

    #Creates Singleton-Variables object from namedtuple


    #Creates Vertex objects from coordinates

    singleton.axiom=[Vertex(np.array([float(v[0]), float(v[1])])) for v in singleton.axiom]
    singleton.border=np.array([singleton.border_x, singleton.border_y])
    print('borders ', singleton.border)

    #Finds the longest possible length of a connection between to vertices
    singleton.maxLength= max(singleton.radiallMax,singleton.gridlMax,singleton.organiclMax,singleton.seedlMax)

    singleton.rule_img, singleton.density_img=input_image_setup(singleton.rule_image_name, singleton.density_image_name)

    with open(path+"/temp/"+singleton.output_name+"_densitymap.txt", 'w') as f:
        f.write(singleton.density_image_name.split(".")[0]+"diffused.png")


    singleton.center=find_radial_centers(singleton)
    singleton.center= [np.array([singleton.border[0] * ((x[1] / singleton.rule_img.shape[1]) - 0.5) * 2, singleton.border[1] * (((singleton.rule_img.shape[0] - x[0]) / singleton.rule_img.shape[0]) - 0.5) * 2]) for x in singleton.center]

    # from procedural_city_generation.roadmap.config_functions.setup_heightmap import setup_heightmap
    # setup_heightmap(singleton, path)


    singleton.global_lists=Global_Lists()
    singleton.global_lists.vertex_list.extend(singleton.axiom)
    singleton.global_lists.coordslist=[x.coords for x in singleton.global_lists.vertex_list]



    def setNeighbours(vertex):
        """ Correctly Sets up the neighbors for a vertex from the axiom.

        Parameters
        ----------
        vertex : vertex Object
        """

        d=np.inf
        neighbour=None
        for v in singleton.axiom:
            if v is not vertex:
                dneu=np.linalg.norm(v.coords-vertex.coords)
                if dneu<d:
                    d=dneu
                    neighbour=v
        vertex.neighbours=[neighbour]

    for k in singleton.axiom:
        setNeighbours(k)

    from scipy.spatial import cKDTree
    singleton.global_lists.tree=cKDTree(singleton.global_lists.coordslist, leafsize=160)

    return singleton
