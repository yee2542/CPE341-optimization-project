from itertools import permutations
from datastruct import readfile, parse_csv, parse_matrix_dist, Place
from random import shuffle, seed, randrange, random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from visualPath import visual
from math import exp, floor, log
import time
from utility import shuffle_list
from perm_index import permutationIndex

REALTIME = True
LOCK_START = True

CONST_N = 10000
CONST_M = 10
CONST_T = 8

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


def sa(data, lockStart=False, realtime=False, verbose=False, typeOfTransit='public'):
    deltaE_avg = 0.0
    n = CONST_N                 # step to lower temp
    m = CONST_M                 # step of each neibor finding solution
    T = CONST_T
    Tinit = T
    distCandidate = fitness(data, typeOfTransit)[0]
    searchSpace = []

    # fraction reduction every cycle
    frac = (1/100)**(1.0/(n-1.0))
    # accept
    p = 0
    na = 0.0
    acceptSolutions = []
    historySolutions = []
    historyT = []

    for i in range(n):
        if verbose:
            print('cycle:', n, 'with temp', T)
            print('m', m * int(floor(deltaE_avg) + 1))
        # for j in range(m * int(floor(deltaE_avg) + 1)):
        # subRound = floor(abs(Tinit - T))
        subRound = m
        for j in range(subRound):
            seed(i)
            if lockStart:
                randomPlace = data[1:]
                randomPlace = shuffle_list(randomPlace)
                data = data[0:1]
                data = data + randomPlace
            else:
                data = shuffle_list(data)

            [dist, h] = fitness(data, typeOfTransit)
            deltaE = abs(distCandidate - dist)
            searchSpace.append((permutationIndex(data), dist))
            if verbose:
                print('dist : distCandidate', dist, distCandidate)

            if dist > distCandidate:
                p = exp(-deltaE / T)  # probability to accept
                # accept worse value
                r = random()
                if verbose:
                    print('random r', r)
                if (r < p):
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
                if realtime and accept == True:
                    plt.pause(0.0000000005)
                    plt.subplot(231)
                    plt.cla()
                    plt.title('distance / nth accepted solution')
                    plt.plot(range(0, len(acceptSolutions)), acceptSolutions,
                             color='green', linewidth=.25, marker='x')

                    plt.subplot(232)
                    plt.title('path solution')
                    plt.cla()
                    visual(historySolutions[-1:][0])

                    plt.subplot(233)
                    plt.cla()
                    plt.title('temperature / nth iteration')
                    plt.ylim(0, Tinit)
                    plt.plot(range(0, len(historyT)), historyT,
                             color='red', linewidth=2)

                    plt.subplot(212)
                    plt.cla()
                    plt.title('search spaces')
                    plt.axvline(x=searchSpace[-1::][0][0])
                    searchSpace.sort(key=lambda e: e[0])
                    nSpace = [i[0] for i in searchSpace]
                    distSpace = [i[1] for i in searchSpace]
                    plt.scatter(nSpace, distSpace, marker=2, alpha=.75)

        historyT.append(T)
        T = frac * T
        if verbose:
            print('prob', p)
            print('na', na)
            print('deltaE', deltaE)

    print('single objective')
    print('number of node', len(data))
    print('type of transit', typeOfTransit)
    print('best distance', min(acceptSolutions))
    print('best distance sa', acceptSolutions[-1:])
    print('best solution sa', historySolutions[-1:][0])

    # plot after finish
    plt.cla()
    plt.subplot(231)
    plt.title('distance / nth accepted solution')
    xplt = list(range(0, len(acceptSolutions), 10))
    xplt.append(len(acceptSolutions))
    plt.plot(xplt, acceptSolutions[::10]+acceptSolutions[-1:],
             color='green', linewidth=.25, marker='x')

    plt.subplot(232)
    plt.title('path solution')
    visualPlt = visual(historySolutions[-1:][0])

    plt.subplot(233)
    plt.title('temperature / nth iteration')
    plt.ylim(0, Tinit)
    plt.plot(range(0, len(historyT)), historyT,
             color='red', linewidth=2)

    plt.subplot(212)
    plt.title('search spaces')
    searchSpace.sort(key=lambda e: e[0])
    nSpace = [i[0] for i in searchSpace]
    distSpace = [i[1] for i in searchSpace]
    plt.scatter(nSpace, distSpace, marker=2, alpha=.15)

    # plt.show()
    return plt


# sa([5, 6, 7, 8, 12])
# sa([1, 3, 4, 5, 6, 7, 8])
# sa([0, 1, 2, 3, 4, 5, 6, 7, 8], True)
# sa([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], True, True)
# sa([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
# sa([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], start=True)
# sa([1, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], lockStart=True, realtime=True)
st_time = time.time()
# saplot = sa([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
#             lockStart=True, realtime=False, typeOfTransit='public')
saplot = sa([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
            lockStart=LOCK_START, realtime=REALTIME, typeOfTransit='public')
ed_time = time.time()
print('exec time', ed_time - st_time, 's')
saplot.show()
