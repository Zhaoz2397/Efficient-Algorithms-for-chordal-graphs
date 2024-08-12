import os
import pickle
import time

from read_dataset import load_single_file
from chordal import is_chordal, chromatic_number_and_max_clique, max_independent_set_and_min_vertex_cover, \
    make_chordal_iter


def measure_execution_time(graph, func, func_name):
    start_time = time.time()
    result = func(graph)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time


def run_algorithms_and_log_results(filename, graph):

    print(f"(\"{filename}\", ", end="")

    for func, func_name in [(is_chordal, 'is_chordal'),
                            (chromatic_number_and_max_clique, 'chromatic_number_and_max_clique'),
                            (max_independent_set_and_min_vertex_cover,
                             'max_independent_set_and_min_vertex_cover')]:
        graph_new = graph.copy()
        if func_name != 'is_chordal':
            graph_new = make_chordal_iter(graph_new)

        num_nodes = graph_new.number_of_nodes()
        num_edges = graph_new.number_of_edges()
        exec_time = measure_execution_time(graph_new, func, func_name)
        result = {
            'Filename': filename,
            'Nodes': num_nodes,
            'Edges': num_edges,
            'Function': func_name,
            'Execution Time (s)': exec_time
        }
        print(f"{num_nodes} + {num_edges}, {exec_time:.6f}, ", end="")
    print("),")


if __name__ == "__main__":
    cache_dir = 'cache'
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    data_dir = './data'

    for file in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file)
        cache_file = os.path.join(cache_dir, f'{file}.pkl')

        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                G = pickle.load(f)
            num_nodes = G.number_of_nodes()
            num_edges = G.number_of_edges()
            # print(f"Loaded cached data for {file}: {num_nodes} nodes, {num_edges} edges")
        else:
            G = load_single_file(file_path)
            num_nodes = G.number_of_nodes()
            num_edges = G.number_of_edges()
            with open(cache_file, 'wb') as f:
                pickle.dump(G, f)
            # print(f"Data cached to {cache_file}")
            # print(f"{file}: {num_nodes} nodes, {num_edges} edges")

        run_algorithms_and_log_results(file, G)
