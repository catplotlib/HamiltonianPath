import random
class Graph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.adjacency_matrix = [[0] * num_vertices for _ in range(num_vertices)]

    def add_edge(self, src, dest):
        if src < 0 or src >= self.num_vertices or dest < 0 or dest >= self.num_vertices:
            raise ValueError("Invalid vertex index")
        self.adjacency_matrix[src][dest] = 1
        self.adjacency_matrix[dest][src] = 1

    def remove_edge(self, src, dest):
        if src < 0 or src >= self.num_vertices or dest < 0 or dest >= self.num_vertices:
            raise ValueError("Invalid vertex index")
        self.adjacency_matrix[src][dest] = 0
        self.adjacency_matrix[dest][src] = 0

    def has_edge(self, src, dest):
        if src < 0 or src >= self.num_vertices or dest < 0 or dest >= self.num_vertices:
            raise ValueError("Invalid vertex index")
        return self.adjacency_matrix[src][dest] == 1

    def get_vertices(self):
        return list(range(self.num_vertices))

    def get_neighbors(self, vertex):
        if vertex < 0 or vertex >= self.num_vertices:
            raise ValueError("Invalid vertex index")
        neighbors = []
        for i in range(self.num_vertices):
            if self.adjacency_matrix[vertex][i] == 1:
                neighbors.append(i)
        return neighbors

    def generate_random_graph(self, edge_probability):
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if random.random() < edge_probability:
                    self.add_edge(i, j)

    def __str__(self):
        graph_str = ""
        for i in range(self.num_vertices):
            row = ""
            for j in range(self.num_vertices):
                row += str(self.adjacency_matrix[i][j]) + " "
            graph_str += row.strip() + "\n"
        return graph_str.strip()

    def check_edge_ends(self):
        # Check connectivity between the first and the last vertex
        return self.has_edge(0, self.num_vertices - 1)
