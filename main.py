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

# def a_star(vertices, visibility_graph):




file_lines = read_file()
vertices, polygons, start, endpoint = populate_data(file_lines)