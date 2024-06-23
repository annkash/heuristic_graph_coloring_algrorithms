import copy
class Graph:
    def __init__(self, vertices=0):
        self.vertices = vertices
        self.edges = 0
        self.adjacency_list = [set() for i in range(0, vertices)]
    def add_edge(self, u, v):
        self.adjacency_list[u - 1].add(v - 1)
        self.adjacency_list[v - 1].add(u - 1)
        self.edges += 1


    def copy(self):
        new = Graph(vertices=self.vertices)
        new.adjacency_list = copy.deepcopy(self.adjacency_list)
        new.edges = self.edges
        return new

    def print(self):
        print('number_of_vertices:', self.vertices ,
              ' number_of_edges:', round(self.edges/2))
        print(self.adjacency_list)

def load_graph(file_path):
    file = open(file_path)
    strings_list = file.readlines()
    for i in range(0, len(strings_list)):
        string = strings_list[i].split()
        if string[0] == 'c':
            continue
        elif string[0] == 'p':
            graph = Graph(int(string[2]))
        elif string[0] == 'e':
            graph.add_edge(int(string[1]), int(string[2]))
    file.close()
    return graph

