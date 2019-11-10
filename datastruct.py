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
        for i in _data:
            self.data[i[0]] = {
                "name": i[1],
                "lat": i[2],
                "lng": i[3]
            }

    def show_place(self):
        print(self.data)


place = readfile('place.csv')
place = parse_csv(place)
# print(place)

dist_public = readfile('dist.public.txt')
dist_public = parse_matrix_dist(dist_public)
print(dist_public)

node = Place(place)
# node.show_place()
