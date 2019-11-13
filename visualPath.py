import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from datastruct import readfile, parse_csv, Place
from pprint import pprint
import networkx as nx
from random import shuffle

def parse_node(d):
    result = []
    for e in d:
        result.append({
            'name': e.get('name'),
            'lat': e.get('lat'),
            'lng': e.get('lng')
        })
    return result

def visual(path, node):
    G = nx.Graph()
    # print('visual', path, node)
    prevNode = node[0]
    nodes = []
    fixed_pos = {}
    edges = []

    # mapped path to edges
    for i, e in enumerate(path):
        fixed_pos[i] = (float(node[i]['lat']), float(node[i]['lng']))
        if i != len(path) - 1:
            edge = (e, path[i + 1])
            edges.append(edge)
        else:
            edge = (e, path[0])
            edges.append(edge)

    G = nx.Graph()
    print('edges', edges)

    G.add_edges_from(edges)
    fixed_nodes = fixed_pos.keys()

    # debugging
    print('fixed pos')
    pprint(fixed_pos)

    print('fixed node')
    pprint(fixed_nodes)

    pos = nx.spring_layout(G, pos=fixed_pos, fixed=fixed_nodes)
    nx.draw_networkx(G, pos)
    plt.show()
    return

node = readfile('place.csv')
node = parse_csv(node)
node = Place(node)
node = parse_node(node.node)

# path = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
path = [0, 1, 2, 3, 4, 5, 6, 7, 8]
# shuffle(path)
visual(path, node)

# visual([0, 1, 2, 3, 4, 5, 6, 7, 8])


# plt.axis([0, 10, 0, 1])

# for i in range(10):
#     y = np.random.random()
#     plt.scatter(i, y)
#     plt.pause(0.0005)

# plt.show()

# import plotly.graph_objects as go

# import networkx as nx

# G = nx.random_geometric_graph(200, 0.125)