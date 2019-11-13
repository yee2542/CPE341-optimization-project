import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from datastruct import readfile, parse_csv, Place
from pprint import pprint
import networkx as nx
from random import shuffle
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def visual(path):

    # self manage data node
    node = readfile('place.csv')
    node = parse_csv(node)
    node = Place(node)

    G = nx.Graph()
    fixed_pos = {}
    edges = []

    # mapped path to edges
    for i, e in enumerate(path):
        # assign fixed node
        positionNode = node.node[e]
        positionNode = (positionNode['lat'], positionNode['lng'])
        fixed_pos[e] = positionNode

    # circular path
        if i != len(path) - 1:
            edge = (e, path[i + 1])
            edges.append(edge)
        else:
            edge = (e, path[0])
            edges.append(edge)

    # init graph object
    G = nx.Graph()
    print('edges', edges)

    G.add_edges_from(edges)
    fixed_nodes = fixed_pos.keys()

    # # debugging
    # print('fixed pos')
    # pprint(fixed_pos)

    # print('fixed node')
    # pprint(fixed_nodes)

    pos = nx.spring_layout(G, pos=fixed_pos, fixed=fixed_nodes)
    nx.draw_networkx(G, pos)
    # plt.show()
    return plt
