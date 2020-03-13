import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import os

def plot_network(edges):

     lc = LineCollection(edges, linewidths=0.5, colors='black')
     fig, ax = plt.subplots()
     ax.add_collection(lc)
     ax.autoscale()
     ax.margins(0.1)
     # path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
     
     plt.savefig("grid1.png")


def generate_grid(grid_len, grid_height, cell_len, cell_height):
    """

    :param grid_len: grid's length
    :param grid_height: grid's width
    :param cell_len: cell's length
    :param cell_height: cell's width
    :return:
    """
    # cols = int(l/a)
    # rows = int(w/b)

    """
    x = np.array([0,1,2]) 
    y = np.array([2,4,6])
    
    take advantage of broadcasting, to make a 2dim array of diffs
    dx = x[..., np.newaxis] - x[np.newaxis, ...]
    dy = y[..., np.newaxis] - y[np.newaxis, ...]
    
    """
    x = np.arange(0, grid_len, cell_len)
    y = np.arange(0, grid_height, cell_height)
    print(x)
    print(y)

    dx = np.abs(x[..., np.newaxis] - x[np.newaxis, ...])
    dy = np.abs(y[..., np.newaxis] - y[np.newaxis, ...])

    print(dx)
    print(dy)
    # m = np.zeros((rows, cols))
    # m = np.array([[j*b+i*a for i in range(cols)] for j in range(rows)])
    #
    # m + m.T - np.diag(m)
    #


def gre(grid_len, grid_height, cell_len, cell_height, p, q):

    cols = int(grid_len/cell_len)
    rows = int(grid_height/cell_height)
    # keep border edges, iterate left to right,bottom  to  top:
    #  - remove horizontal  edge with prob (1−p)
    #  - remove vertical edge e(i,0)(i,1) with the probab p(1−p)
    #  - remove a vertical edge e(i,j)(i,j+1) with probability (1−p) if exists e(i,j)(i+1,j)
    # For each vertex where both i and j are odd, generate diagonal edges with the probability q.
    edges = []
    edges.extend([((i, 0), (i+1, 0)) for i in range(rows)])
    edges.extend([((i, cols),(i+1, cols)) for i in range(rows)])
    # vertical borders
    edges.extend([((0, i), (0, i+1)) for i in range(cols)])
    edges.extend([((rows, i), (rows, i+1)) for i in range(cols)])

    edges = set([])
    for i in range(1, rows):
        for j in range(1, cols):
   # horizontal edges
            if np.random.uniform() > p:
                edges.add(((i,j),(i+1,j)))

            # vertical edges
            if j == 0 and np.random.uniform() > p*(1-p):
                edges.add(((i,j),(i,j+1)))

            if j > 0 and not ((i,j),(i+1)) in edges and np.random.uniform() > p:
                edges.add(((i,j),(i,j+1)))

            # diagonals
            if np.random.uniform() > q:
                edges.add(((i,j),(i+1, j+1)))
            if np.random.uniform() > q:
                 edges.add(((i,j),(i-1, j-1)))
            if np.random.uniform() > q:
                edges.add(((i,j),(i-1, j+1)))
            if np.random.uniform() > q:
                edges.add(((i,j),(i+1, j-1)))

    plot_network(edges)

gre(10, 10, 0.2, 0.3, 0.35, 0.56)