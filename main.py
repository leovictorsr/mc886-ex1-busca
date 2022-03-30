from itertools import groupby
import math

def calculateDistance(start, endpoint):

    return ((start[0] - endpoint[0])**2 + (start[1] - endpoint[1])**2)**0.5

def calculateDistance(start, endpoint):

    return ((start[0] - endpoint[0])**2 + (start[1] - endpoint[1])**2)**0.5

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
        vertices['start'] = tuple(break_lines[2][0].split())
        vertices['endpoint'] = tuple(break_lines[2][1].split())
        start = tuple(break_lines[2][0].split())
        start = tuple([float(start[0]), float(start[1])])
        endpoint = tuple(break_lines[2][1].split())
        endpoint = tuple([float(endpoint[0]), float(endpoint[1])])

        return (vertices, polygons)

def verify_intersection(p1, p2, p3, p4):
    max_x = max([p1[0], p2[0]])
    min_x = min([p1[0], p2[0]])
    if not (min_x <= p3[0] <= max_x or min_x <= p4[0] <= max_x):
        return 0
    
    max_y = max([p1[1], p2[1]])
    min_y = min([p1[1], p2[1]])
    if not (min_y <= p3[1] <= max_y or min_y <= p4[1] <= max_y ):
        return 0
    
    return 1

def line_equation(p1, p2):
    try:
        m = (p2[1] - p1[1]) / (p2[0] - p1[0])
        n = p2[1] - m*p2[0]
        y = lambda x: m*x + n
    except ZeroDivisionError:
        y = lambda x: p2[0]

    return y

def children_graph(vertices, polygons):
    children_dict = {}
    vertices_list = vertices.keys()
    edge_list = {}

    for i, polygon in polygons.items():
        for j in range(len(polygon) - 1):
            func = line_equation(vertices[polygon[j]], vertices[polygon[j+1]])
            edge_list[polygon[j]+polygon[j+1]] = func
            try:
                children_dict[polygon[j]].append(polygon[j+1])
            except:
                children_dict[polygon[j]] = [polygon[j+1]]
                pass
            try:
                children_dict[polygon[j+1]].append(polygon[j])
            except:
                children_dict[polygon[j+1]] = [polygon[j]]
                pass
        
    for vertice, position in vertices.items():
        for vert in vertices_list:
            if vert == vertice: continue
            if vert in children_dict[vertice]: continue
            for edge in edge_list.keys():
                print(edge)
                print(vertice, vert)
                is_inter = verify_intersection(vertices[edge[0]], vertices[edge[1]], vertices[vertice], vertices[vert])

                print(is_inter)
    print(children_dict)

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

print('Start point: ', start)
print('End point: ', endpoint)

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
