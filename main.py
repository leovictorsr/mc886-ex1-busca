from http.client import NotConnected
from importlib.resources import path
from itertools import groupby
import math

# SETUP FUNCTIONS
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
        vertices[name] = tuple([float(a), float(b)])

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
        vertices['start'] = tuple([float(x) for x in break_lines[2][0].split()])
        vertices['endpoint'] = tuple([float(x) for x in break_lines[2][1].split()])

        return (vertices, polygons)

# VISIBILITY FUNCTIONS
def does_intersect(a, b, c, d, p, q, r, s):
    det = (c - a) * (s - q) - (r - p) * (d - b)
    if (det == 0):
        return 0
    else:
        lambda_ = ((s - q) * (r - a) + (p - r) * (s - b)) / det
        gamma = ((b - d) * (r - a) + (c - a) * (s - b)) / det
        return ((0 < lambda_ and lambda_ < 1) and (0 < gamma and gamma < 1)) * 1


def is_visible(vertices, polygons):
    vertices_list = vertices.keys()
    visible = {}
    edge_list = []
    for polygon in polygons.values():
        for j in range(len(polygon) - 1):
            edge_list.append(polygon[j]+polygon[j+1])
            try:
                visible[polygon[j]].append(polygon[j+1])
            except:
                visible[polygon[j]] = [polygon[j+1]]
                pass
            try:
                visible[polygon[j+1]].append(polygon[j])
            except:
                visible[polygon[j+1]] = [polygon[j]]
    
    polygon_dict = {}

    xB = -10
    yB = 1000
    for i, polygon in polygons.items():
        for vertex in polygon:
            polygon_dict[vertex] = i
            xAaux = vertices[vertex][0]
            yAaux = vertices[vertex][1]
            for vertex_2 in polygon:
                if vertex == vertex_2: continue
                if vertex_2 in visible[vertex]: continue
                counter = 0
                xBaux = vertices[vertex_2][0]
                yBaux = vertices[vertex_2][1]
                xA = (xAaux + xBaux) / 2
                yA = (yAaux + yBaux) / 2
                for edge in edge_list:
                    xC = vertices[edge[0]][0]
                    yC = vertices[edge[0]][1]
                    xD = vertices[edge[1]][0]
                    yD = vertices[edge[1]][1]
                    is_inter = does_intersect(xA, yA, xB, yB, xC, yC, xD, yD)
                    is_inter = does_intersect(xA, yA, xB, yB, xC, yC, xD, yD)
                    if is_inter:
                        counter += 1
                if counter%2 == 0:
                    try:
                        visible[vertex].append(vertex_2)
                    except:
                        visible[vertex] = [vertex_2]
                    try:
                        visible[vertex_2].append(vertex)
                    except:
                        visible[vertex_2] = [vertex]

    polygon_dict['start'] = -1
    polygon_dict['endpoint'] = -2

    for vertice in vertices_list:
        xA = vertices[vertice][0]
        yA = vertices[vertice][1]
        for vert in vertices_list:
            if vert == vertice: continue
            if vertice in visible.keys() and vert in visible[vertice]: continue
            if polygon_dict[vert] == polygon_dict[vertice]: continue
            xB = vertices[vert][0]
            yB = vertices[vert][1]
            intersect = []
            for edge in edge_list:
                xC = vertices[edge[0]][0]
                yC = vertices[edge[0]][1]
                xD = vertices[edge[1]][0]
                yD = vertices[edge[1]][1]
                is_inter = does_intersect(xA, yA, xB, yB, xC, yC, xD, yD)
                intersect.append(is_inter)
                if is_inter: 
                    break
            if 1 not in intersect:
                try:
                    visible[vertice].append(vert)
                except:
                    visible[vertice] = [vert]
                try:
                    visible[vert].append(vertice)
                except:
                    visible[vert] = [vertice]
    return visible

# A* FUNCTIONS
def euclidian_distance(a, b):
    distance = math.sqrt(pow(b[0] - a[0], 2) + pow(b[1] - a[1], 2))
    return distance

def a_star_calculate_weights(visible_to_current, current_name, acc_weight, vertices):
    # get current vertex coordinates
    current = vertices[current_name]

    # generate a list with accumulated weights to all visible vertices
    new_weights = list(map(
        lambda x: (x, acc_weight + euclidian_distance(current, vertices[x])),
        visible_to_current
    ))

    weight_dict = {}
    for w in new_weights:
        weight_dict[w[0]] = {
            'weight': w[1]
        }

    return weight_dict


def a_star_select_lower(current_tree, current_path):
    min_value = float('inf')

    for adjacent in current_tree['adjacents']:
        adjacent_path = current_path.copy()
        adjacent_path.append(adjacent)
        current_tree['adjacents'][adjacent]['path'] = adjacent_path

        if 'adjacents' not in current_tree['adjacents'][adjacent]:
            vertex = adjacent
            value = current_tree['adjacents'][adjacent]['weight']
            path = current_tree['adjacents'][adjacent]['path']
        else:
            vertex, value, path = a_star_select_lower(current_tree['adjacents'][adjacent], current_tree['adjacents'][adjacent]['path'])

        if value < min_value and vertex not in current_path:
            min_value = value
            selected_vertex = vertex
            selected_path = path
    
    return selected_vertex, min_value, selected_path


def a_star(vertices, visibility_graph):
    visible_to_current = visibility_graph['start']
    selected_vertex = 'start'
    weights_tree = {
        'start': {
            'weight': 0,
            'path': ['start'],
            'adjacents': {}
        }
    }
    selected_path = ['start']

    while ('endpoint' not in visible_to_current):
        current_tree = weights_tree
        for p in selected_path:
            if p == 'start':
                current_tree = current_tree[p]
            else:
                current_tree = current_tree['adjacents'][p]

        current_tree['adjacents'] = a_star_calculate_weights(visible_to_current, selected_vertex, current_tree['weight'], vertices)
        selected_vertex, min_weight, selected_path = a_star_select_lower(weights_tree['start'], ['start'])
        visible_to_current = visibility_graph[selected_vertex]

    min_weight += euclidian_distance(vertices[selected_vertex], vertices['endpoint'])
    return min_weight, selected_path

# BFS FUNCTIONS
def calculateDistance(start, endpoint):
    return ((start[0] - endpoint[0])**2 + (start[1] - endpoint[1])**2)**0.5
def costOfTheWay(best):
    cost = 0
    for i in range(len(best) - 1):
        cost += calculateDistance(vertices[best[i]], vertices[best[i+1]])
    return cost

def costOfTheWay(best):
    cost = 0
    for i in range(len(best) - 1):
        cost += calculateDistance(vertices[best[i]], vertices[best[i+1]])
    return cost

def bfs(vertices, graph, start, endpoint):
    visited = {}
    queue = []
    best = []
    queue.append('start')
    visited[start] = True

    while queue:
        vertex = queue.pop(0)

        if vertex == 'endpoint':
            return best

        shorterDistance = calculateDistance(start, endpoint)
        bestNeighbor = graph[vertex][0]

        for neighbor in graph[vertex]:
            if neighbor in visited:
                continue

            distance = calculateDistance(vertices[neighbor], endpoint)
            if distance < shorterDistance:
                shorterDistance = distance
                bestNeighbor = neighbor
                visited[neighbor] = True
        queue.append(bestNeighbor)
        best.append(bestNeighbor)
    return best

# READ FILE AND TREAT DATA
file_lines = read_file()
vertices, polygons = populate_data(file_lines)

# BUILD VISIBILITY GRAPH
visible_graph = is_visible(vertices, polygons)

# RUN FOR BFS
best = bfs(vertices, visible_graph, vertices['start'], vertices['endpoint'])
weight = costOfTheWay(best)
print('BFS :: Custo total :: ', weight)
print('BFS :: Caminho :: ', ('*' + ''.join(best) + '*').replace('endpoint', ''))
print('BFS :: N. de vértices percorridos :: ', len(best) - 1)
print()

# RUN FOR A*
weight, path = a_star(vertices, visible_graph)
print('A* :: Custo total :: ', weight)
print('A* :: Caminho :: ', ' -> '.join(path) + ' -> endpoint')
print('A* :: N. de vértices percorridos :: ', len(path) - 1)
print()
