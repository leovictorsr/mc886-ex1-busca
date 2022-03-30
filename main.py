from itertools import groupby

def calculate_distance(start, endpoint):
    return abs(start[0] - endpoint[0]) + abs(start[1] - endpoint[1])

def read_file():
    file_lines = []

    with open('ex1-dados.txt', 'r') as f:
        for line in f:
            file_lines.append(line.strip())

    return file_lines

def read_vertices(raw_vertices):
    vertices = {}

    for vertex in raw_vertices:
        name, a, b = vertex.split()
        vertices[name] = tuple([a, b])

    return vertices

def read_polygons(raw_polygons):
    polygons = {}

    for polygon in raw_polygons:
        name = polygon.split()[0]
        polygons[name] = ''.join(polygon.split()[1:])

    return polygons


def populate_data(file_lines):
    break_lines = [list(group) for line, group in groupby(file_lines, key = bool) if line]
    if break_lines and len(break_lines) == 3:
        vertices = read_vertices(break_lines[0])
        polygons = read_polygons(break_lines[1])
        start = tuple(break_lines[2][0].split())
        endpoint = tuple(break_lines[2][1].split())

        return (vertices, polygons, start, endpoint)


file_lines = read_file()
vertices, polygons, start, endpoint = populate_data(file_lines)

print(vertices)

print(polygons)

print('Start point: ', start)
print('End point: ', endpoint)