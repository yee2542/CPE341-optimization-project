def circular_path(path=[]):
    edges = []
    for i, e in enumerate(path):
        if i != len(path) - 1:
            edge = (e, path[i + 1])
            edges.append(edge)
        else:
            edge = (e, path[0])
            edges.append(edge)
    return edges
