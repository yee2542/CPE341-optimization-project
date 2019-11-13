from itertools import permutations
from datastruct import readfile, parse_csv, parse_matrix_dist, Place
from random import shuffle, seed, randrange, random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from visualPath import visual

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

# c = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
c = [0, 1, 2, 3, 4, 5, 6, 7, 8]
shuffle(c)
print(c)

bestDist = 9999
history = []
loop = range(0, 200)
for i in loop:
    [dist, h] = fitness(c)
    history.extend(h)
    def randSeed():
        return .25
        # return .1

    # shuffle(c, randSeed)
    shuffle(c)
    if dist < bestDist:
        bestDist = dist
        print('found best new dist', dist)
print('dist', bestDist)

# print('history',len(history))
# plt.plot(loop, history, color='green', linewidth = 1, marker='x')
# plt.legend() 
# plt.show()
# print(history[-14:])

from math import exp, floor

def sa(data):
    bestDist = 9999999
    history = []
    deltaE_avg = 0.0
    n = 130                 # step to lower temp
    m = 50                 # step of each neibor finding solution
    T = 20
    distCandidate = fitness(data)[0]
    # fraction reduction every cycle
    frac = (1/100)**(1.0/(n-1.0))
    # accept
    p = 0
    na = 0.0
    acceptSolutions = []
    historySolutions = []

    def randSeed():
        return .1

    for i in range(n):
        print('cycle:', n, 'with temp', T)
        print('m', m * int(floor(deltaE_avg) + 1))
        # for j in range(m * int(floor(deltaE_avg) + 1)):
        for j in range(m):
            # print(seed(j))
            shuffle(data)
            # shuffle(data, randSeed)
            [dist, h] = fitness(data)
            # print('dist', dist)
            history.extend(h)
            # deltaE = abs(dist -  distCandidate)
            deltaE = abs(distCandidate - dist)
            if dist < distCandidate:
                if (j == 0 and i == 0):
                    deltaE_avg = deltaE
                p = exp(-deltaE/(deltaE_avg / T)) # probability to accept
                # accept worse value
                if (random() < p):
                    accept = True
                else:
                    accept = False
            # obj function is lower, automatically accept
            else:
                accept = True
            
            if accept == True:
                # print('accept solution', dist)
                acceptSolutions.append(dist)
                historySolutions.append(data)
                # update currently accept solution
                distCandidate = dist
                # increment number of accept solution
                na = na + 1.0
                deltaE_avg = (deltaE_avg * (na-1.0) +  deltaE) / na
        T = frac * T
        print('prob', p)
        print('na', na)
        print('deltaE', deltaE)
    # print(len(acceptSolution))
    print('best distance', min(acceptSolutions))
    print('best solution', historySolutions[-1:])
    # print('accept solution', acceptSolution)
    plt.plot(range(0, len(acceptSolutions)), acceptSolutions, color='green', linewidth = .5, marker='x')
    # plt.legend() 
    # plt.show()
    # print('visualNode', visualNode)
    # visual(historySolutions[-1:])
    # visual([1,2,4])
    # plt.show()



# sa([0, 1, 2, 3, 4, 5, 6, 7, 8])
sa([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])


