import random
from itertools import combinations

import networkx as nx
from collections import defaultdict

from tqdm import tqdm


# Union-Find Implementation
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [1] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1


def classify(graph):
    class_ = [0] * len(graph.nodes())
    class_map = {}
    cnt = 0

    uf = UnionFind(len(graph.nodes()))
    node_index = {n: i for i, n in enumerate(graph.nodes())}

    for u, v in graph.edges():
        uf.union(node_index[u], node_index[v])

    for node in graph.nodes():
        root = uf.find(node_index[node])
        if root not in class_map:
            class_map[root] = cnt
            cnt += 1
        class_[node_index[node]] = class_map[root]

    return class_


def make_chordal(graph):
    # Traverse each node in the graph
    for node in list(graph.nodes()):

        # Use Union-Find for classification
        uf = UnionFind(len(graph.nodes()))
        node_index = {n: i for i, n in enumerate(graph.nodes())}

        for u, v in graph.edges():
            if u != node and v != node:
                uf.union(node_index[u], node_index[v])

        neighbor_classes = defaultdict(list)
        for neighbor in list(graph.neighbors(node)):
            root = uf.find(node_index[neighbor])
            neighbor_classes[root].append(neighbor)

        # For points of the same category, connect these points into clusters
        for neighbors in neighbor_classes.values():
            for u, v in combinations(neighbors, 2):
                if u != v:
                    graph.add_edge(u, v)

    self_loops = list(nx.selfloop_edges(graph))
    graph.remove_edges_from(self_loops)

    assert nx.is_chordal(graph)



def gen_graph(n, p):
    G = nx.gnp_random_graph(n, p)
    return G


def gen_chordal(n, p):
    G = nx.gnp_random_graph(n, p)
    make_chordal(G)
    return G


def gen_weighted_chordal(n, p):
    G = nx.gnp_random_graph(n, p)
    components = list(nx.connected_components(G))
    for i in range(len(components) - 1):
        comp1 = components[i]
        comp2 = components[i + 1]
        node1 = random.choice(list(comp1))
        node2 = random.choice(list(comp2))
        G.add_edge(node1, node2)

    make_chordal(G)
    for node in G.nodes():
        G.nodes[node]['weight'] = random.randint(1, 1)
    return G


if __name__ == '__main__':
    G = gen_chordal(1000, 0.0015)
    # print("Chordal Graph nodes:", G.nodes())
    # print("Chordal Graph edges:", G.edges())
    print("Is Chordal Graph:", nx.is_chordal(G))

    from chordal import is_chordal

    print("Is Chordal Graph:", is_chordal(G))
