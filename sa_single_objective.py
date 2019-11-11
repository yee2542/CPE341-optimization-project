from itertools import permutations
from datastruct import readfile, parse_csv, parse_matrix_dist, Place
from random import shuffle, seed, randrange, random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

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

node.transit_info_name('public', 1, 4)
node.transit_info_name('public', 4, 1)
node.get_place(1)
node.search_place('สยาม')

perm = [1, 2, 3, 4, 5, 6, 7, 8]
# perm = permutations(perm)

# print('generated permu')
# print(list(perm))

# for i in list(perm):
#     print(i)

def fitness(d = []):
    maxLength = len(d)
    totalDist = 0
    history = []
    for i, e in enumerate(d):
        if i < maxLength - 1:
            dist = node.transit_info_id('public', e, d[i+1]).get('dist')
        else:
            dist = node.transit_info_id('public', e, d[0]).get('dist')
        totalDist += dist
    history.append(totalDist)
    # print('total dist', totalDist)
    return [totalDist, history]

c = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
shuffle(c)
print(c)

bestDist = 9999
history = []
loop = range(0, 100)
for i in loop:
    # seed(i)
    [dist, h] = fitness(c)
    history.extend(h)
    def randSeed():
        # return .00001
        return .5

    shuffle(c, randSeed)
    # shuffle(c)
    if dist < bestDist:
        bestDist = dist
        print('found best new dist', dist)
print('dist', bestDist)

# print('history',len(history))
plt.plot(loop, history, color='green', linewidth = 1, marker='x')
plt.legend() 
plt.show()


