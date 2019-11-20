from itertools import permutations
from datastruct import readfile, parse_csv, parse_matrix_dist, Place
import time

node = readfile('place.csv')
node = parse_csv(node)

dist_taxi = readfile('dist.taxi.txt')
dist_taxi = parse_matrix_dist(dist_taxi, True)

dist_public = readfile('dist.public.txt')
dist_public = parse_matrix_dist(dist_public)

DATA_FIELD = ['dist', 'time', 'cost']
node = Place(node)
node.add_matrix(dist_taxi, 'taxi', DATA_FIELD)
node.add_matrix(dist_public, 'public', DATA_FIELD)


def fitness(d=[], typeOfTransit='public'):
    maxLength = len(d)
    totalDist = 0
    history = []
    for i, e in enumerate(d):
        if i < maxLength - 1:
            dist = node.transit_info_id(typeOfTransit, e, d[i+1]).get('dist')
        else:
            dist = node.transit_info_id(typeOfTransit, e, d[0]).get('dist')
        totalDist += dist
    history.append(totalDist)
    return [totalDist, history]


def allSolution(placeNode):
    listPerm = permutations(placeNode)
    # print(listPerm)
    bestDistance = 9999999
    lockNode = [0]
    bestSolution = []

    for e in list(listPerm):
        solution = list(e)
        if solution[0] == lockNode[0]:
            dist = fitness(solution)[0]
            if dist < bestDistance:
                bestDistance = dist
                bestSolution = solution
    return [bestDistance, bestSolution]


placeNode = [0, 1, 2, 3, 4, 5, 6, 7]
st_time = time.time()
[bestDistance, bestSolution] = allSolution(placeNode)
ed_time = time.time()
print('permutation')
print('number of node', len(bestSolution))
print('best distance', bestDistance)
print('solution', bestSolution)
print('exec time', ed_time - st_time, 's')

