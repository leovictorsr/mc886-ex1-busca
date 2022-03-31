from itertools import groupby

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
        start = tuple(break_lines[2][0].split())
        start = tuple([float(start[0]), float(start[1])])
        endpoint = tuple(break_lines[2][1].split())
        endpoint = tuple([float(endpoint[0]), float(endpoint[1])])

        return (vertices, polygons, start, endpoint)


file_lines = read_file()
vertices, polygons, start, endpoint = populate_data(file_lines)

print(vertices)

print(polygons)

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
