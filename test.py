import unittest
import time
import networkx as nx

from chordal import is_chordal, chromatic_number_and_max_clique, max_independent_set_and_min_vertex_cover
from gen_chordal import gen_chordal, gen_graph


def measure_time(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return result, end_time - start_time


class MyTestCase(unittest.TestCase):

    def test_chordal_graph(self):
        small_times = []
        large_times = []

        for i in range(1000):
            G = gen_chordal(50, 0.2)
            result, duration = measure_time(is_chordal, G)
            small_times.append(duration)
            self.assertEqual(result, nx.is_chordal(G))
            if (i + 1) % 100 == 0:
                print(f"[Chordal Graph] {i + 1} tests completed")

        for i in range(10):
            G = gen_chordal(1000, 0.0015)
            result, duration = measure_time(is_chordal, G)
            large_times.append(duration)
            self.assertEqual(result, nx.is_chordal(G))
            print(f"[Big Chordal Graph] {i + 1} tests completed")

        print(f"Average time for small chordal graph: {sum(small_times) / len(small_times):.6f} seconds")
        print(f"Average time for large chordal graph: {sum(large_times) / len(large_times):.6f} seconds")

    def test_random_graph(self):
        small_times = []
        large_times = []

        for i in range(1000):
            G = gen_graph(50, 0.2)
            result, duration = measure_time(is_chordal, G)
            small_times.append(duration)
            self.assertEqual(result, nx.is_chordal(G))
            if (i + 1) % 100 == 0:
                print(f"[Not Chordal Graph] {i + 1} tests completed")

        for i in range(10):
            G = gen_graph(1000, 0.0015)
            result, duration = measure_time(is_chordal, G)
            large_times.append(duration)
            self.assertEqual(result, nx.is_chordal(G))
            print(f"[Big Not Chordal Graph] {i + 1} tests completed")

        print(f"Average time for small not chordal graph: {sum(small_times) / len(small_times):.6f} seconds")
        print(f"Average time for large not chordal graph: {sum(large_times) / len(large_times):.6f} seconds")

    def test_chromatic_number(self):
        small_times = []
        large_times = []

        for i in range(1000):
            G = gen_chordal(50, 0.2)
            self.assertEqual(nx.is_chordal(G), True)
            coloring = nx.coloring.greedy_color(G, strategy="largest_first")
            chromatic_number = max(coloring.values()) + 1
            result, duration = measure_time(chromatic_number_and_max_clique, G)
            small_times.append(duration)
            self.assertEqual(result, chromatic_number)
            if (i + 1) % 100 == 0:
                print(f"[Chromatic Number] {i + 1} tests completed")

        for i in range(10):
            G = gen_chordal(1000, 0.0015)
            coloring = nx.coloring.greedy_color(G, strategy="largest_first")
            chromatic_number = max(coloring.values()) + 1
            result, duration = measure_time(chromatic_number_and_max_clique, G)
            large_times.append(duration)
            self.assertEqual(result, chromatic_number)
            print(f"[Big Chromatic Number] {i + 1} tests completed")

        print(f"Average time for small chromatic number: {sum(small_times) / len(small_times):.6f} seconds")
        print(f"Average time for large chromatic number: {sum(large_times) / len(large_times):.6f} seconds")

    def test_max_independent_set(self):
        small_times = []
        large_times = []

        for i in range(1000):
            G = gen_chordal(50, 0.2)
            G_complement = nx.complement(G)
            max_clique = max(nx.find_cliques(G_complement), key=len)
            result, duration = measure_time(max_independent_set_and_min_vertex_cover, G)
            small_times.append(duration)
            self.assertEqual(result, len(max_clique))
            if (i + 1) % 100 == 0:
                print(f"[Max Independent Set] {i + 1} tests completed")

        for i in range(10):
            G = gen_chordal(1000, 0.0015)
            result, duration = measure_time(max_independent_set_and_min_vertex_cover, G)
            large_times.append(duration)
            print(result)
            print(f"[Big Max Independent Set] {i + 1} tests completed")

        print(f"Average time for small max independent set: {sum(small_times) / len(small_times):.6f} seconds")
        print(f"Average time for large max independent set: {sum(large_times) / len(large_times):.6f} seconds")


if __name__ == '__main__':
    unittest.main()
