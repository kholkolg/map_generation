from proc_model.additional_stuff.Singleton import Singleton
import matplotlib.pyplot as plt

plotbool = False

singleton = Singleton("roadmap")


class Vertex(object):
    """
    Vertex (name after mathematical graph-theory) object used in roadmap submodule.
    Has the following attributes:
    - coords : numpy.ndarray(2, )
        XY-Coordinates of this Vertex
    - neighbours : list<procedural_city_generation.roadmap.Vertex>
        List of all Vertices that this Vertex is currectly connected to (has a road to)
    - minor_road : boolean
        Describes whether this road is a minor road
    - seed : boolean
        Describes whether this (major) road is a seed
    """

    def __init__(self, coords):
        """
        Parameters
        ----------
        coords : numpy.array(2, )
            XY-Coordinates of this Vertex

        """
        self.id = '-'.join([str(x) for x in coords])
        self.coords = coords
        self.neighbours = []
        self.minor_road = False
        self.seed = False

    def __cmp__(self, other):
        if isinstance(other, Vertex):
            if self.coords[0] > other.coords[0]:
                return 1
            elif self.coords[0] < other.coords[0]:
                return -1
            else:
                if self.coords[1] > other.coords[1]:
                    return 1
                elif self.coords[1] < other.coords[1]:
                    return -1
            return 0

    def __getitem__(self, i):
        return self.coords[i]


    def connect(self, other):
        """
        Manages connections so that no Vertex has two connections to
        the same other Vertex. Also responsible for plotting this Vertex
        in matplotlib if the "plot" parameter in /inputs/roadmap.conf
        is set to True.

        Parameters
        ----------
        other : procedural_city_generation.roadmap.Vertex object
            The vertex that this vertex is goint to be connected to.
        """
        # print('connect ', self, ' ', other)
        if other not in self.neighbours:
            self.neighbours.append(other)
        if self not in other.neighbours:
            other.neighbours.append(self)


    def __repr__(self):
        return "Vertex{}".format(self.coords)


