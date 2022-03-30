from itertools import groupby

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
        endpoint = tuple(break_lines[2][1].split())

        return (vertices, polygons, start, endpoint)

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

file_lines = read_file()
vertices, polygons, start, endpoint = populate_data(file_lines)
children_graph(vertices, polygons)
print(vertices)

print(polygons)

print('Start point: ', start)
print('End point: ', endpoint)