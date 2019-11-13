from pprint import pprint


def readfile(path):
    f = open(path, "r")
    content = f.read()
    return content


def parse_csv(data=''):
    line = data.splitlines()  # split each line to list
    result = []
    for i in line:
        row = i.split(',')  # split each row to sub list
        result.append(row)
    return result[1:]  # cut header out


def parse_matrix_dist(data='', reversible=False):
    parse = data.splitlines()
    result = []
    if reversible:
        # if parse reversible file
        for r, e in enumerate(parse):  # append data to result first
            result.append(e.split('\t'))
        for r, re in enumerate(result):  # transpose matrix
            if r > 0:
                for c, ce in enumerate(re):
                    result[r][c] = result[c][r]
                    if ce == '0':  # if found 0 brake transpose op
                        break
        return result
    else:
        for e in parse:  # split by tab
            result.append(e.split('\t'))
        return result


class Place:
    def __init__(self, _data):
        self.node = []
        self.matrix = {}
        for i in _data:
            self.node.append({
                "name": i[1].strip(),
                "lat": float(i[2].strip()),
                "lng": float(i[3].strip())
            })

    def show_place(self):
        print(self.node)

    def show_matrix(self):
        print('show matrix')
        pprint(self.matrix)

    def get_place(self, id=0):
        data = self.node[id]
        pprint(data)
        return data

    def search_place(self, name):
        for e in self.node:
            found = e.get('name')
            if found == name:
                pprint(e)
                return e

    def add_matrix(self, data, name='', field=[]):      # for adding matrix relation
        if len(self.node) == 0:
            return Exception('must declare with place data fist')
        self.matrix[name] = []
        for e in data:
            row = []
            for i, n in enumerate(e):
                contain = n.split(',')
                mapping = {}
                if contain[0] != '0':
                    # loop through fields for setting data struct for each node
                    for fi, f in enumerate(field):
                        mapping[f] = float(contain[fi])
                else:
                    # if found 0 set everything in dict = 0
                    for fi, f in enumerate(field):
                        mapping[f] = float(0)
                row.append(mapping)
            # append mapping to self class
            self.matrix[name].append(row)

    def transit_info_id(self, type_of_transit, start, stop, verbose=False):
        # query from distance matrix
        data = self.matrix[type_of_transit][start][stop]
        if verbose:
            print('from (ID) : ', start, '-->', 'dest (ID) : ', stop)
            pprint(data)
        return data

    def transit_info_name(self, type_of_transit, start, stop, verbose=False):
        data = self.matrix[type_of_transit][start][stop]
        from_place = self.node[start].get('name')       # map ID to node name
        dest_place = self.node[stop].get('name')
        if verbose:
            print('from : ', from_place, '-->', 'dest : ', dest_place)
            pprint(data)
        return data


DATA_FIELD = ['dist', 'time', 'cost']

# read data node and parse (place)
place = readfile('place.csv')
place = parse_csv(place)

# read matrix and parse distance for public
dist_public = readfile('dist.public.txt')
dist_public = parse_matrix_dist(dist_public)

# read matrix and parse distance for taxi
dist_taxi = readfile('dist.taxi.txt')
# this file have to set True cause will fill a left value
dist_taxi = parse_matrix_dist(dist_taxi, True)

# initialize class
node = Place(place)
node.add_matrix(dist_public, 'public', DATA_FIELD)
node.add_matrix(dist_taxi, 'taxi', DATA_FIELD)

# example
# node.show_place()
# node.transit_info_id('taxi', 1, 4)
# node.transit_info_name('taxi', 1, 4)
# node.transit_info_name('taxi', 4, 1)
