from itertools import permutations


def getperm(index, generator):
    aux = 0
    for j in generator:
        if aux == index:
            return j
        else:
            aux = aux + 1


class LexicoGraphPermu:
    def __init__(self, _arr):
        self.arr = _arr

    def getNPerm(self, n):
        p = list(getperm(n, permutations(self.arr)))
        return p
