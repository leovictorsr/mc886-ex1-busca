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

        return (vertices, polygons)

def verify_intersection(p1, p2, p3, p4):
    max_x = max([p1[0], p2[0]])
    min_x = min([p1[0], p2[0]])
    if not (min_x <= p3[0] <= max_x or min_x <= p4[0] <= max_x):
        return 0
    
    max_y = max([p1[1], p2[1]])
    min_y = min([p1[1], p2[1]])
    if not (min_y <= p3[1] <= max_y or min_y <= p4[1] <= max_y ):
        vertices['start'] = tuple(map(int,break_lines[2][0].split()))
        vertices['endpoint'] = tuple(map(int,break_lines[2][1].split()))
        return (vertices, polygons)

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

vertices, polygons = populate_data(file_lines)

visible_graph = is_visible(vertices, polygons)
print(vertices)

print(polygons)

print(visible_graph)
