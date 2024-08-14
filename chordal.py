from collections import defaultdict
from heapq import heappush as push, heappop as pop
import random

import networkx as nx


class MaxTuple:
    def __init__(self, tup):
        self.tup = tup

    def __lt__(self, other):
        return self.tup > other.tup

    def __eq__(self, other):
        return self.tup == other.tup

    def __repr__(self):
        return repr(self.tup)


def lex_bfs(graph):
    ordering = []
    marked = set()

    buckets = defaultdict(list)
    node_lex = {node: [] for node in graph.nodes()}
    deque_c = []

    n = len(graph)

    def add_bucket(lex: list, node_id: int):
        lex = tuple(lex)
        buckets[lex].append(node_id)
        if len(buckets[lex]) == 1:
            push(deque_c, MaxTuple(lex))

    def get_node():
        node = -1
        while node == -1 or node in marked:
            lex = pop(deque_c).tup
            node = buckets[lex].pop()
            if not buckets[lex]:
                del buckets[lex]
            else:
                push(deque_c, MaxTuple(lex))

        return node

    for node in graph.nodes():
        add_bucket(node_lex[node], node)

    for i in range(n, 0, -1):
        node = get_node()
        marked.add(node)
        ordering.append(node)

        if len(ordering) == n:
            break

        for neighbor in graph.neighbors(node):
            if neighbor not in marked:
                node_lex[neighbor].append(i)
                add_bucket(node_lex[neighbor], neighbor)

    return ordering


def is_chordal(graph):
    ordering = lex_bfs(graph)
    ord_map = {node: i for i, node in enumerate(ordering)}

    marked = set()

    graph_edge = {node: set(graph.neighbors(node)) for node in graph.nodes()}

    for node in ordering:
        marked.add(node)
        neighbors = list(graph_edge[node] & marked)

        mx_idx = 0
        for i in range(1, len(neighbors)):
            if ord_map[neighbors[i]] > ord_map[neighbors[mx_idx]]:
                mx_idx = i

        for i in range(len(neighbors)):
            if i != mx_idx and neighbors[mx_idx] not in graph_edge[neighbors[i]]:
                return False

    return True
def chromatic_number_and_max_clique(G):
    order = lex_bfs(G)
    n = len(order)
    color = [-1] * (max(G.nodes()) + 1)
    for i in range(n):
        node = order[i]
        neighbors_color = set()
        for neighbor in G.neighbors(node):
            if neighbor > n:
                continue
            if color[neighbor] != -1:
                neighbors_color.add(color[neighbor])
        for j in range(n):
            if j not in neighbors_color:
                if node > n:
                    continue
                color[node] = j
                break
    return max(color) + 1

def maximum_clique_chordal(graph):
    ordering = lex_bfs(graph)
    c_max = set()
    visited = set()

    for v in ordering:
        if v in visited:
            continue
        neighbors = {u for u in graph.neighbors(v) if ordering.index(u) > ordering.index(v)}
        c = {v} | neighbors
        visited.update(c)
        if len(c) > len(c_max):
            c_max = c

    return c_max


def max_independent_set_and_min_vertex_cover(G):
    order = lex_bfs(G)[::-1]
    n = len(order)
    vis = [False] * (max(G.nodes()) + 1)

    independent_set = []

    for i in range(n):
        node = order[i]
        if vis[node] is False:
            independent_set.append(node)
            neighbors = list(G.neighbors(node))
            for neighbor in neighbors:
                if vis[neighbor] is False:
                    vis[neighbor] = True

    return len(independent_set)


def maximum_independent_set(graph):

    ord = lex_bfs(graph)
    dp = {v: {v} for v in graph.nodes()}

    for v in reversed(ord):
        max_set = dp[v]

        for u in graph.nodes():
            if u != v and not graph.has_edge(v, u) and ord.index(u) > ord.index(v):

                potential_set = dp[u] | {v}

                if all(not graph.has_edge(x, y) for x in potential_set for y in potential_set if x != y):
                    if len(potential_set) > len(max_set):
                        max_set = potential_set
        dp[v] = max_set
        print(f"DP[{v}] updated to: {dp[v]}")
    s_max = max(dp.values(), key=len)
    return s_max



def complement_graph2choral(graph):
    ordering = lex_bfs(graph)
    ord_map = {node: i for i, node in enumerate(ordering)}

    marked = set()

    graph_edge = {node: set(graph.neighbors(node)) for node in graph.nodes()}

    pair = set()

    for node in ordering:
        marked.add(node)
        neighbors = list(graph_edge[node] & marked)

        mx_idx = 0
        for i in range(1, len(neighbors)):
            if ord_map[neighbors[i]] > ord_map[neighbors[mx_idx]]:
                mx_idx = i

        for i in range(len(neighbors)):
            if i != mx_idx and neighbors[mx_idx] not in graph_edge[neighbors[i]]:
                pair.add((neighbors[mx_idx], neighbors[i]))

    for u, v in pair:
        graph.add_edge(u, v)


def random_subgraph(G, fraction=0.1):
    if not 0 < fraction <= 1:
        raise ValueError("Fraction should be between 0 and 1.")
    nodes = list(G.nodes())
    num_nodes_to_keep = int(len(nodes) * fraction)
    nodes_to_keep = random.sample(nodes, num_nodes_to_keep)
    subgraph = G.subgraph(nodes_to_keep).copy()

    return subgraph


def make_chordal_from_cliques(graph):
    marked = set()

    for clique in nx.find_cliques(graph):
        if any(node in marked for node in clique):
            continue

        for node in clique:
            marked.add(node)

    subgraph = graph.subgraph(list(marked)).copy()

    return subgraph


def make_chordal_iter(graph):
    while len(graph.nodes()) > 10000 or len(graph.edges()) > 50000:
        graph = random_subgraph(graph, random.uniform(0.7, 0.9))

    graph = make_chordal_from_cliques(graph)

    while not is_chordal(graph):
        # print("graph", graph.number_of_edges())
        complement_graph2choral(graph)

        if len(graph.edges()) > 50000:
            graph = random_subgraph(graph, random.uniform(0.7, 0.9))

    return graph

if __name__ == "__main__":

    from gen_chordal import gen_graph, make_chordal, UnionFind

    G0 = gen_graph(1000, 0.0015)
    print(is_chordal(G0), nx.is_chordal(G0))
    while not is_chordal(G0):
        complement_graph2choral(G0)
        print(G0.number_of_edges())
    print(is_chordal(G0), nx.is_chordal(G0))


    G = nx.Graph()
    edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5)]
    # edges = [(0, 1), (0, 4), (1, 5), (2, 3)]
    # edges = [(0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5)]

    G.add_edges_from(edges)

    print("Graph nodes:", G.nodes())
    print("Graph edges:", G.edges())

    ordering = lex_bfs(G)
    print("Lexicographic BFS ordering:", ordering)

    print("Is chordal:", is_chordal(G), nx.is_chordal(G))

    coloring = nx.coloring.greedy_color(G, strategy="largest_first")
    chromatic_number = max(coloring.values()) + 1
    print("Chromatic number:", chromatic_number_and_max_clique(G), chromatic_number)

    G_complement = nx.complement(G)

    max_clique = nx.find_cliques(G_complement)
    max_clique = max(max_clique, key=len)

    print("Max independent set:", max_independent_set_and_min_vertex_cover(G), len(max_clique))
    G = nx.Graph()
    edges = [(1, 2), (1, 3), (1, 4), (2, 3), (3, 4), (4, 5)]
    G.add_edges_from(edges)

