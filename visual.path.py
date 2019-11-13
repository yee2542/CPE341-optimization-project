import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from datastruct import readfile, parse_csv, Place
from pprint import pprint
import networkx as nx
from random import shuffle


node = readfile('place.csv')
node = parse_csv(node)
node = Place(node)


def parse_node(d):
    result = []
    for e in d:
        result.append({
            'name': e.get('name'),
            'lat': e.get('lat'),
            'lng': e.get('lng')
        })
    return result


node = parse_node(node.node)
print('node', node)


def visual(path, node):
    G = nx.Graph()
    # print('visual', path, node)
    prevNode = node[0]
    nodes = []
    fixed_pos = {}
    edges = []

    for i, e in enumerate(path):
        if i != len(path) - 1:
            nextNode = node[e]
            fixed_pos[i] = (float(nextNode.get('lat')), float(nextNode.get('lng')))
            edge = (e, path[i + 1])
            edges.append(edge)
        else:
            edge = (e, path[0])
            edges.append(edge)
        # else:
        #     print('yathhhhhhh')

    # for i, e in enumerate(path):
    #     if i != len(path) - 1:
    #         nextNode = node[e + 1]
    #         result.append({
    #             'node': e,
    #             'start': prev,
    #             'stop': nextNode
    #         })
    #         prev = nextNode
    #     else:
    #         result.append({
    #             'node': e,
    #             'start': prev,
    #             'stop': node[0]
    #         })
    G=nx.Graph()
    print('edges', edges)

    G.add_edges_from(edges) #define G
    # fixed_pos = {1:(150.3,5),2:(-1,2)}#dict with two of the positions set
    fixed_nodes = fixed_pos.keys()
    print('fixed pos')
    pprint(fixed_pos)

    print('fixed node')
    pprint(fixed_nodes)

    pos = nx.spring_layout(G,pos=fixed_pos, fixed = fixed_nodes)
    nx.draw_networkx(G,pos)

    plt.show()

    return


# visual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], node)
path = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
shuffle(path)
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
