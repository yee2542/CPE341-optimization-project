from itertools import permutations
from datastruct import readfile, parse_csv, parse_matrix_dist, Place
from random import shuffle, seed, randrange, random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from visualPath import visual
from math import exp, floor

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


def fitness(d=[]):
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
# c = [0, 1, 2, 3, 4, 5, 6, 7, 8]


def sa(data, realtime=False):
    bestDist = 9999999
    history = []
    deltaE_avg = 0.0
    n = 50                 # step to lower temp
    m = 25                 # step of each neibor finding solution
    T = 10
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
                p = exp(-deltaE/(deltaE_avg / T))  # probability to accept
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
                deltaE_avg = (deltaE_avg * (na-1.0) + deltaE) / na

                # realtime plot
                if realtime:
                    plt.subplot(121)
                    plt.pause(0.0000000005)
                    plt.plot(range(0, len(acceptSolutions)), acceptSolutions,
                             color='green', linewidth=.5, marker='x')
                    plt.subplot(122)
                    plt.cla()
                    visual(historySolutions[-1:][0])

        T = frac * T
        print('prob', p)
        print('na', na)
        print('deltaE', deltaE)

    # print(len(acceptSolution))
    print('best distance', min(acceptSolutions))
    print('best solution', historySolutions[-1:][0])
    # print('accept solution', acceptSolution)

    # plt.legend()
    # plt.show()
    # print('visualNode', visualNode)

    # plot after finish
    if realtime == False:
        plt.subplot(121)
        plt.plot(range(0, len(acceptSolutions)), acceptSolutions,
                color='green', linewidth=.5, marker='x')

        plt.subplot(122)
        visualPlt = visual(historySolutions[-1:][0])
        visualPlt.show()

    plt.show()


# sa([1, 3, 4, 5, 6, 7, 8])
sa([0, 1, 2, 3, 4, 5, 6, 7, 8], True)
# sa([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
