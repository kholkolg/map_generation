import pandas as pd
import osmnx as ox
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
import scipy.stats as stats



def edge_length(graph):

    lengths = np.array([x['length'] for _, x in graph.edges.items()])
    # lengths.sort()
    avg = lengths.mean()
    dev = lengths.std()
    # n = len(lengths)
    # lens = np.array(lengths)
    print('length: min=', min(lengths),', max=', max(lengths), ', mean=',avg, ', sigma=',dev)

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(24, 8))

    axes[0].hist(lengths, 100, density=True)
    x = np.linspace(min(lengths), max(lengths), 100)
    axes[0].plot(x, stats.norm.pdf(x, avg, dev))
    # plt.plot(x, stats.alpha.pdf(x, a=0.001))
    in_degrees = np.array([d for e, d in graph.in_degree])
    avg = in_degrees.mean()
    dev = in_degrees.std()
    print('InDegree min=', min(in_degrees),', max=', max(in_degrees), ', mean=',avg, ', sigma=',dev)

    axes[1].hist(in_degrees, 5, density=True)
    x = np.linspace(min(in_degrees), max(in_degrees), 10)
    axes[1].plot(x, stats.norm.pdf(x, avg, dev))

    out_degrees = np.array([d for e, d in graph.out_degree])
    avg = out_degrees.mean()
    dev = out_degrees.std()
    print('OutDegree min=', min(out_degrees), ', max=', max(out_degrees), ', mean=', avg, ', sigma=', dev)

    axes[2].hist(out_degrees, 5, density=True)
    x = np.linspace(min(out_degrees), max(out_degrees), 10)
    axes[2].plot(x, stats.norm.pdf(x, avg, dev))

    plt.show()

    return avg, dev

city = 'Prague'
filename = city.lower()+'.graphml'

try:
    G = ox.load_graphml(filename)

except FileNotFoundError:
    print('File not found. Downloading graph')
    G = ox.graph_from_place(city, network_type='drive', simplify=True)
    ox.save_graphml(G, filename=filename)

print('Num nodes=', G.number_of_nodes(), ', num edges=', G.number_of_edges())
# ox.plot_graph(G)
# edge_dict = {e['osm_id']:{'length': e['length']} for _, e in G.edges.items()}
# print(edge_dict)
G_proj = ox.project_graph(G)

# edges = [(e[0], e[1]) for e in G_proj.edges]
# edges.sort()
# # print(edges[:10])
# print(len(edges), print(len(set(edges))))

# c=0
# for e, d in G.in_degree:
#     if isinstance(e, list):
#         print(e, d)
#         c += 1
    # if c == 10: break
# edge_length(G)

# basic stats
# 'n': , 'm': ,'k_avg': ,
# 'edge_length_total': ,
# 'edge_length_avg': ,
# 'node_density_km': ,
# 'edge_density_km': ,
# 'circuity_avg': ,

#
# nodes_proj = ox.graph_to_gdfs(G_proj, edges=False)
# graph_area = nodes_proj.unary_union.convex_hull.area
stat = ox.extended_stats(G, connectivity=True, cc=True, ecc=True, bc=True) #
stat = {k:v for k,v in stat if isinstance(v, float) or isinstance(v, int)}
for k, v in stat.items():
    # if isinstance(v, float) or isinstance(v, int):
    print(k, v)
# stat = ox.basic_stats(G, area=graph_area, clean_intersects=True, circuity_dist='euclidean')
# stat['area_m2'] = graph_area
# stat['city'] = city
#
# to_remove = ['streets_per_node_avg', 'streets_per_node_proportion','street_length_total','street_length_avg',
#              'street_segments_count', 'street_density_km', 'self_loop_proportion','clean_intersection_count',
#             'clean_intersection_density_km', 'intersection_count' ]
# columns = ['n', 'm', 'k_avg', 'edge_length_total', 'edge_length_avg',
#            'node_density_km','edge_density_km']
# df = pd.DataFrame(stat)
# df.drop(columns=[c for c in df.columns if c not in columns], inplace=True)
# df.rename(columns={'n':'num_nodes', 'm':'num_edges', 'k_avg':'degree_avg'} ,inplace=True)
# print(df)

# # print(ox.extended_stats(G))





############################################
# basic stats
# 'n': ,
# 'm': 48396,
# 'k_avg': 4.648991354466859,
# 'edge_length_total': 5781894.219000002,
# 'edge_length_avg': 119.47049795437644,
# 'node_density_km': 37.397970185900114,
# 'edge_density_km': 10385.740039394348,
# 'circuity_avg': 89603.92146050588,

# 'intersection_count': 17174, 'streets_per_node_avg': 2.8131123919308356,
# 'streets_per_node_counts': {0: 0, 1: 3646, 2: 451, 3: 13030, 4: 3551, 5: 126, 6: 15, 7: 1},
#  'streets_per_node_proportion': {0: 0.0, 1: 0.1751200768491835, 2: 0.021661863592699327, 3: 0.6258405379442843,
# 4: 0.17055715658021134, 5: 0.006051873198847263, 6: 0.0007204610951008645, 7: 4.803073967339097e-05},
# 'street_length_total': 3573819.9640000057,
# 'street_length_avg': 122.04418823208024,
#  'street_segments_count': 29283,
# 'intersection_density_km': 30.848834772941814,
#  'street_density_km': 6419.481866640098,
# 'self_loop_proportion': 0.0034093726754277215,
#  'clean_intersection_count': 1,
#  'clean_intersection_density_km': 0.0017962521703122052,