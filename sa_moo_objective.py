from itertools import permutations
from datastruct import readfile, parse_csv, parse_matrix_dist, Place
from random import shuffle, seed, randrange, random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from visualPath import visual
from math import exp, floor, log
import time
from utility import shuffle_list, gerateMultiTypeSearchSpace
from perm_index import permutationIndex


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

REALTIME = False

MAX_DELTA_COST = 50
MAX_DELTA_KM = 1
MAX_COST_PER_TRIP = 200

CONST_N = 10000
CONST_M = 10
CONST_T = 8


def fitness(d=[], typeOfTransit='public'):
    maxLength = len(d)
    totalDist = 0
    totalCost = 0
    history = []
    arrTrace = []
    taxiPath = []
    pubPath = []
    for i, e in enumerate(d):
        if i < maxLength - 1:
            distPub = node.transit_info_id('public', e, d[i+1]).get('dist')
            costPub = node.transit_info_id('public', e, d[i+1]).get('cost')
            distTax = node.transit_info_id('taxi', e, d[i+1]).get('dist')
            costTax = node.transit_info_id('taxi', e, d[i+1]).get('cost')
            arrTrace.append({
                'node': (e, d[i+1]),
                'pub': [distPub, costPub],
                'taxi': [distTax, costTax]
            })
        else:
            distPub = node.transit_info_id('public', e, d[0]).get('dist')
            costPub = node.transit_info_id('public', e, d[0]).get('cost')
            distTax = node.transit_info_id('taxi', e, d[0]).get('dist')
            costPub = node.transit_info_id('taxi', e, d[0]).get('cost')
            arrTrace.append({
                'node': (e, d[0]),
                'pub': [distPub, costPub],
                'taxi': [distTax, costPub]
            })

        # totalDistPub += distPub
        # totalDistTax += distTax
    # history.append(totalDistPub)
    # print('arr trace', arrTrace)
    minimumTotal = 0

    for i in arrTrace:
        pubDist = i.get('pub')[0]
        pubCost = i.get('pub')[1]
        taxiDist = i.get('taxi')[0]
        taxiCost = i.get('taxi')[1]
        deltaDist = abs(pubDist - taxiDist)
        deltaCost = pubCost - taxiCost
        if(deltaDist <= MAX_DELTA_KM):
            # print('compare', deltaDist)
            if(deltaCost >= MAX_DELTA_COST and pubCost < taxiCost):
                totalDist += pubDist
                totalCost += pubCost
                history.append({'type': 'pub', 'result': i.get('pub')})
                pubPath.append(i.get('node'))

            else:
                totalDist += taxiDist
                totalCost += taxiCost
                history.append({'type': 'taxi', 'result': i.get('taxi')})
                taxiPath.append(i.get('node'))
        else:
            if(taxiCost <= MAX_COST_PER_TRIP):
                totalDist += taxiDist
                totalCost += taxiCost
                history.append({'type': 'taxi', 'result': i.get('taxi')})
                taxiPath.append(i.get('node'))
            else:
                totalDist += pubDist
                totalCost += pubCost
                history.append({'type': 'pub', 'result': i.get('pub')})
                pubPath.append(i.get('node'))

        # print(deltaDist, deltaCost)
    #     pub = i.get('pub')[0]
    #     tax = i.get('tax')[0]
    #     if(pub < tax):
    #         minimumTotal += pub
    #         history.append(pub)
    #     else:
    #         minimumTotal += tax
    #         history.append(tax)
    # print(history)
    # print('total', totalDist, totalCost)
    return [totalDist, totalCost, history, pubPath, taxiPath]


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
    acceptCosts = []
    historyT = []
    historyCost = []

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

            [dist, cost, h, pubPath, taxiPath] = fitness(data, typeOfTransit)

            deltaE = abs(distCandidate - dist)
            multiSearchSpace = gerateMultiTypeSearchSpace(data, h, dist)
            # debugging
            # print('multi search sapce', multiSearchSpace)
            # print(permutationIndex(multiSearchSpace), gerateMultiTypeSearchSpace(data, h, dist))
            searchSpace.append((permutationIndex(multiSearchSpace), dist))
            if verbose:
                print('dist : distCandidate', dist, distCandidate)
                print('cost : ', cost)
                print('pubpath', pubPath)
                print('taxiPath', taxiPath)

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
                historyCost.append(cost)
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
                    plt.plot(range(0, len(historyCost)), historyCost,
                             color='orange', linewidth=.25, marker='x')

                    plt.subplot(232)
                    plt.title('path solution')
                    plt.cla()
                    visual(historySolutions[-1:][0], pubPath, taxiPath)

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
    print('best cost sa', cost)
    print('path solution', h)

    # plot after finish
    plt.cla()
    plt.subplot(231)
    plt.title('distance / nth accepted solution')
    xplt = list(range(0, len(acceptSolutions), 10))
    xplt.append(len(acceptSolutions))
    plt.plot(xplt, acceptSolutions[::10]+acceptSolutions[-1:],
             color='green', linewidth=.25, marker='x')
    # plt.plot(range(0, len(historyCost)), historyCost,
    #          color='orange', linewidth=.25, marker='x')

    plt.subplot(232)
    plt.title('path solution')
    visualPlt = visual(historySolutions[-1:][0], pubPath, taxiPath)

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
            lockStart=True, realtime=REALTIME, typeOfTransit='public')
ed_time = time.time()
print('exec time', ed_time - st_time, 's')
saplot.show()
