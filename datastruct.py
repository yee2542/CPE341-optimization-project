def readfile(path):
    f = open(path, "r")
    content = f.read()
    print(content)
    return content


def parse_csv(data=''):
    line = data.splitlines()  # split each line to list
    result = []
    for i in line:
        row = i.split(',')  # split each row to sub list
        result.append(row)
    return result[1:]  # cut header out


def parse_matrix_dist(data='', reversable=False):
    parse = data.splitlines()
    result = []
    for i, e in enumerate(parse):
        result.append(e.split('\t'))
    return result


class Place:
    def __init__(self, _data):
        self.data = {}
        self.matrix = {}
        for i in _data:
            self.data[i[0]] = {
                "name": i[1],
                "lat": i[2],
                "lng": i[3]
            }

    def show_place(self):
        print(self.data)

    def show_matrix(self):
        print('show matrix')
        print()
        print(self.matrix)

    def add_matrix(self, data, name='', field=[]):
        if len(self.data.keys()) == 0:
            return Exception('must declare with place data fist')
        self.matrix[name] = []
        for e in data:
            node = []
            for i, n in enumerate(e):
                contain = n.split(',')
                mapping = {}
                if contain[0] != '0':
                    for fi, f in enumerate(field):
                        mapping[f] = float(contain[fi])
                else:
                    for fi, f in enumerate(field):
                        mapping[f] = float(0)
                node.append(mapping)
                print('contain', contain)
                print('mapping',mapping)
                print(len(node),node)
            self.matrix[name].append(node)



place = readfile('place.csv')
place = parse_csv(place)
# print(place)

dist_public = readfile('dist.public.txt')
dist_public = parse_matrix_dist(dist_public)
print(dist_public)

node = Place(place)
node.add_matrix(dist_public, 'public', ['dist', 'time', 'cost'])
node.show_matrix()
test = node.matrix.get('public')
print(test)
print(test[0][2])
# node.show_place()
