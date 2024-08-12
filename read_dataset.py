import os
import gzip
import tarfile
import networkx as nx
import pickle


def load_single_file(file_path):
    G = nx.Graph()
    if file_path.endswith('.tar.gz'):
        with tarfile.open(file_path, 'r:gz') as tar:
            for member in tar.getmembers():
                if member.isfile() and member.name.endswith('.txt'):
                    with tar.extractfile(member) as f:
                        for line in f:
                            if not line.startswith('#'):
                                try:
                                    u, v = map(int, line.decode('utf-8').split()[:2])
                                    G.add_edge(u, v)
                                except ValueError:
                                    print(f"Skipping invalid line in {file_path}: {line}")
    elif file_path.endswith('.txt.gz'):
        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            for line in f:
                if not line.startswith('#'):
                    try:
                        u, v = map(int, line.split()[:2])
                        G.add_edge(u, v)
                    except ValueError:
                        print(f"Skipping invalid line in {file_path}: {line}")
    elif file_path.endswith('.csv.gz'):
        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            next(f)  # Skip header
            for line in f:
                try:
                    u, v, *rest = line.strip().split(',')
                    G.add_edge(int(u), int(v))
                except ValueError:
                    print(f"Skipping invalid line in {file_path}: {line}")
    return G


def load_snap_data(data_dir, cache_dir='cache'):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    results = []

    for file in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file)
        cache_file = os.path.join(cache_dir, f'{file}.pkl')

        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                G = pickle.load(f)
            num_nodes = G.number_of_nodes()
            num_edges = G.number_of_edges()
            print(f"Loaded cached data for {file}: {num_nodes} nodes, {num_edges} edges")
        else:
            G = load_single_file(file_path)
            num_nodes = G.number_of_nodes()
            num_edges = G.number_of_edges()
            with open(cache_file, 'wb') as f:
                pickle.dump(G, f)
            print(f"Data cached to {cache_file}")
            print(f"{file}: {num_nodes} nodes, {num_edges} edges")

        results.append((file, G))

    return results


if __name__ == "__main__":
    data_directory = './data'
    snap_data_info = load_snap_data(data_directory)

    for filename, G in snap_data_info:
        num_nodes = G.number_of_nodes()
        num_edges = G.number_of_edges()
        print(f"{filename}: {num_nodes} nodes, {num_edges} edges")
