import matplotlib.pyplot as plt
from pprint import pprint
# import networkx as nx

# G = nx.Graph()
# G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
# # G.add_edge(1, 2)
# G.add_edges_from([(1, 2), (1, 3), (2, 3)])

# node_sizes = [3 + 10 * i for i in range(len(G))]
# N = G.number_of_nodes()
# M = G.number_of_edges()
# edge_colors = range(2, M + 2)
# edge_alphas = [(5 + i) / (M + 4) for i in range(M)]

# print('n', N)
# # nx.draw_shell(G, nlist=[range(0, N), range(N + 1)], with_labels=True, font_weight='bold')
# nx.draw(G)
# plt.show()

import networkx as nx
G = nx.Graph()
G.add_edges_from([(1, 2), (2, 3), (3, 1), (1, 4), (5, 6)])  # define G
# dict with two of the positions set
fixed_positions = {1: (13, 2), 3: (1, 2), 2: (0, 0)}
fixed_nodes = fixed_positions.keys()

print('pos')
pprint(fixed_positions)

print('nodes')
pprint(fixed_nodes)
pos = nx.spring_layout(G, pos=fixed_positions, fixed=fixed_nodes)
nx.draw_networkx(G, pos)
plt.show()
