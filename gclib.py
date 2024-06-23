import graphlib as gl
import random
from queue import Queue
import heapq
from timeit import default_timer
def greedy_color(graph: gl.Graph, K: list) -> list:
    colors = [-1 for i in range(graph.vertices)]
    color = 0
    colors[K[0]] = color
    isavailable = [True for i in range(graph.vertices)]
    for v_vertex in K[1:len(K)]:
        for u_vertex in graph.adjacency_list[v_vertex]:
            if (colors[u_vertex] != -1):
                isavailable[colors[u_vertex]] = False
        for col in range(graph.vertices):
            if ((isavailable[col] == True) and (col <= color)):
                colors[v_vertex] = col
                break
            if ((isavailable[col] == True) and (col > color)):
                color += 1
                colors[v_vertex] = color
                break
        isavailable = [True for i in range(graph.vertices)]
    return colors

def rs_color(graph: gl.Graph) -> list:
    K = [i for i in range(graph.vertices)]
    random.shuffle(K)
    return greedy_color(graph, K)

def lf_color(graph: gl.Graph) ->list:
    graph_degrees = {i: len(graph.adjacency_list[i])
                     for i in range(graph.vertices)}
    max_degree = max(graph_degrees.values())
    degrees = [[] for i in range(max_degree + 1)]
    for vertex, degree in graph_degrees.items():
        degrees[degree].append(vertex)
    K = [vertex for degree in range(max_degree + 1) for vertex in degrees[degree]]
    return greedy_color(graph, K[::-1])

def sl_color(graph: gl.Graph) -> list:
    K = []
    subgraph = {i: graph.adjacency_list[i] for i in range(graph.vertices)}
    while (len(subgraph)):
        vertex = min(subgraph.items(), key=lambda x: len(x[1]))[0]
        K.append(vertex)
        adjacent_vertices = subgraph[vertex].copy()
        for u_vertex in adjacent_vertices:
            subgraph[u_vertex].remove(vertex)
        subgraph.pop(vertex)
    return greedy_color(graph, K[::-1])

def cs_color(graph: gl.Graph) -> list:
    K = []
    K.append(0)
    queue = Queue()
    visited = [False] * graph.vertices
    visited[0] = True
    queue.put(0)
    while (not queue.empty()):
        vertex = queue.get()
        for neighbor in graph.adjacency_list[vertex]:
            if not (visited[neighbor]):
                visited[neighbor] = True
                queue.put(neighbor)
                K.append(neighbor)
    return greedy_color(graph, K)

def DSATUR(graph: gl.Graph) -> list:
    colors = [-1 for i in range(graph.vertices)]
    graph_degrees = \
        [len(graph.adjacency_list[i]) for i in range(graph.vertices)]
    graph_saturations = [set() for i in range(graph.vertices)]
    color = 0
    uncolored = []
    for vertex in range(graph.vertices):
        heapq.heappush\
            (uncolored, ((-1)*len(graph_saturations[vertex]),
                         (-1)*graph_degrees[vertex], vertex))
    while (len(uncolored) != 0):
        sat, deg, vertex = heapq.heappop(uncolored)
        vertices = len(uncolored)
        for i in range(vertices):
            u_sat, u_deg, u_vertex = heapq.heappop(uncolored)
            heapq.heappush\
                (uncolored, ((-1) * len(graph_saturations[u_vertex]),
                             (-1) * graph_degrees[u_vertex], u_vertex))
        isavailable = [True for i in range(graph.vertices)]
        for u_vertex in graph.adjacency_list[vertex]:
            if (colors[u_vertex] != -1):
                isavailable[colors[u_vertex]] = False
        for col in range(graph.vertices):
            if ((isavailable[col] == True) and (col <= color)):
                colors[vertex] = col
                break
            if ((isavailable[col] == True) and (col > color)):
                color += 1
                colors[vertex] = color
                break
        for u_vertex in graph.adjacency_list[vertex]:
            if (colors[u_vertex] == -1):
                heapq.heappush\
                    (uncolored, ((-1)*len(graph_saturations[u_vertex]),
                                 (-1)*graph_degrees[u_vertex], u_vertex))
                graph_saturations[u_vertex].add(colors[vertex])
                graph_degrees[u_vertex] -= 1
    return colors

def GIS_color(graph: gl.Graph):
    colors = [-1 for i in range(graph.vertices)]
    color = 0
    while (any(vertex == -1 for vertex in colors)):
        subgraph = \
            {i: [vertex for vertex in graph.adjacency_list[i]
                    if colors[vertex] == -1] for i in range(graph.vertices)
             if (colors[i] == -1)}
        while (len(subgraph) != 0):
            vertex = min(subgraph.items(), key=lambda x: len(x[1]))[0]
            colors[vertex] = color
            adjacent_vertices = subgraph[vertex].copy()
            for u_vertex in adjacent_vertices:
                for v_vertex in subgraph[u_vertex]:
                    subgraph[v_vertex].remove(u_vertex)
                subgraph.pop(u_vertex)
            subgraph.pop(vertex)
        color += 1
    return colors

if __name__ == '__main__':
    begin = default_timer()
    graph = gl.load_graph('DSJC250.1.col')
    print(len(set(sl_color(graph))))
    end = default_timer()
    print("elapsed time: ", end - begin)
