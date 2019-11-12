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

from math import exp

def sa(data):
    bestDist = 9999999
    history = []
    deltaE_avg = 0.0
    n = 200                 # step to lower temp
    m = 50                 # step of each neibor finding solution
    T = 10.0
    distC = fitness(data)[0]
    # fraction reduction every cycle
    frac = (1/100)**(1.0/(n-1.0))
    # accept
    na = 0.0
    acceptSolution = []
    
    for i in range(n):
        print('cycle:', n, 'with temp', T)
        for j in range(m):
            shuffle(data)
            [dist, h] = fitness(data)
            history.extend(h)
            deltaE = abs(dist -  distC)
            if dist < distC:
                if (j == 0 and i == 0):
                    deltaE_avg = deltaE
                p =  exp(-deltaE/(deltaE_avg / T)) # probability to accept
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
                acceptSolution.append(dist)
                # update currently accept solution
                distC = dist
                # increment number of accept solution
                na = na + 1.0
                deltaE_avg = (deltaE_avg * (na-1.0) +  deltaE) / na
        T = frac * T
        print('na', na)
    # print(len(acceptSolution))
    print('best distance', min(acceptSolution))
    # print('accept solution', acceptSolution)
    plt.plot(range(0, len(acceptSolution)), acceptSolution, color='green', linewidth = 1, marker='x')
    # plt.legend() 
    plt.show()



# sa([0, 1, 2, 3, 4, 5, 6, 7, 8])
sa([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])


