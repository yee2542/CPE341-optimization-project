from datastruct import readfile, parse_csv, parse_matrix_dist, Place

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

