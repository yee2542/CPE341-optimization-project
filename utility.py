from random import shuffle


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


def shuffle_list(some_list):
    randomized_list = some_list[:]
    while True:
        shuffle(randomized_list)
        for a, b in zip(some_list, randomized_list):
            if a == b:
                break
        else:
            return randomized_list


def generateTypePath(n=1, sym=[0], ns=[1]):
    arr = []
    # for i in range(n):
    for ix, e in enumerate(sym):
            for n in range(ns[ix]):
                arr.append(e)

    return arr

def gerateMultiTypeSearchSpace(data, h, fitness):
    arr = []
    for i, e in enumerate(h):
        t = e.get('type')
        d = data[i]
        if t == 'pub':
            arr.append(-1)
        else:
            arr.append(-2)
        arr.append(d)
    return arr

def prettierMMO(arr=[{}]):
    typeT = []
    dist = []
    cost = []
    for e in arr:
        typeT.append(e.get('type'))
        dist.append(e.get('result')[0])
        cost.append(e.get('result')[1])
    print('type : ',typeT)
    print('dist : ',dist)
    print('cost : ',cost)

