from itertools import permutations
from datastruct import readfile, parse_csv, parse_matrix_dist, Place
from random import shuffle, seed, randrange, random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from visualPath import visual
from math import exp, floor
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

    # accept
    acceptSolutions = []
    historySolutions = []
    historyT = []
    distCandidate = 99999
    n = 10000

    for i in range(n):
        if lockStart:
            randomPlace = data[1:]
            shuffle(randomPlace)
            data = data[0:1]
            data = data + randomPlace
        else:
            shuffle(data)

        [dist, h] = fitness(data, typeOfTransit)

        if dist < distCandidate:
            accept = True
        else:
            accept = False


        if accept == True:
            # print('accept solution', dist)
            acceptSolutions.append(dist)
            historySolutions.append(data)
            # update currently accept solution
            distCandidate = dist

            # realtime plot
            if realtime:
                plt.pause(0.0000000005)
                plt.subplot(131)
                plt.title('distance / nth accepted solution')
                plt.plot(range(0, len(acceptSolutions)), acceptSolutions,
                         color='green', linewidth=.25, marker='x')

                plt.subplot(132)
                plt.title('path solution')
                plt.cla()
                visual(historySolutions[-1:][0])

                plt.subplot(133)
                plt.title('temperature / nth iteration')
                plt.ylim(0, Tinit)
                plt.plot(range(0, len(historyT)), historyT,
                         color='red', linewidth=2)

    print('single objective hill climbing')
    print('number of node', len(data))
    print('type of transit', typeOfTransit)
    # print('best distance', min(acceptSolutions))
    print('best distance sa', acceptSolutions[-1:])
    print('best solution sa', historySolutions[-1:][0])

    # plot after finish
    plt.subplot(131)
    plt.title('distance / nth accepted solution')
    plt.plot(range(0, len(acceptSolutions)), acceptSolutions,
             color='green', linewidth=.25, marker='x')

    plt.subplot(132)
    plt.title('path solution')
    visualPlt = visual(historySolutions[-1:][0])

    # plt.subplot(133)
    # plt.title('temperature / nth iteration')
    # plt.ylim(0, Tinit)
    # plt.plot(range(0, len(historyT)), historyT,
    #          color='red', linewidth=2)

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
            lockStart=True, realtime=False, typeOfTransit='public')
ed_time = time.time()
print('exec time', ed_time - st_time, 's')
# saplot.show()
