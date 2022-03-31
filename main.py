from itertools import groupby
import math

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
        vertices['start'] = tuple(break_lines[2][0].split())
        vertices['endpoint'] = tuple(break_lines[2][1].split())

        return (vertices, polygons)


def euclidian_distance(a, b):
    distance = math.sqrt(pow(b[0] - a[0]) + pow(b[1] - a[1]))
    return distance

def calculate_move(visible_to_current, current_name, acc_weight, vertices):
    # get current vertex coordinates
    current = vertices[current_name]

    # generate a list with accumulated weights to all visible vertices
    weights = visible_to_current.map(lambda x: acc_weight + euclidian_distance(current, x))

    # git minimum accumulated value, its index and its label
    min_weight = min(weights)
    index_min_weight = min(range(len(weights)), key=weights.__getitem__)
    selected_vertex = visible_to_current[index_min_weight]

    return selected_vertex, min_weight


def a_star(vertices, visibility_graph):
    current = visibility_graph['start']
    current_name = 'start'
    path = '*'
    acc_weight = 0

    while (current != visibility_graph['endpoint']):
        next_move, acc_weight = calculate_move(current, current_name, acc_weight, vertices)
        path += next_move
        current = visibility_graph[next_move]
        current_name = next_move

    return path

file_lines = read_file()
vertices, polygons, start, endpoint = populate_data(file_lines)