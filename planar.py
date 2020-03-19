import networkx as nx
from matplotlib import pyplot as plt

G = nx.PlanarEmbedding()
G.add_half_edge_cw(0, 1, None)
G.add_half_edge_cw(0, 2, 1)
G.add_half_edge_cw(0, 3, 2)
G.add_half_edge_cw(1, 0, None)
G.add_half_edge_cw(2, 0, None)
G.add_half_edge_cw(3, 0, None)



nx.draw_networkx(G)
plt.show()