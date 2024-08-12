import matplotlib.pyplot as plt
import numpy as np

# Data from the provided log
datasets = [
    ("facebook_combined.txt.gz", 4039, 88234, 0.234001, 703, 12728, 0.030000, 478, 9804, 0.015001,),
    ("soc-Epinions1.txt.gz", 75879, 405740, 2.828923, 5451, 29199, 0.123677, 6906, 33067, 0.093002,),
    ("soc-sign-bitcoinalpha.csv.gz", 3782, 14123, 0.030000, 789, 34703, 0.106002, 838, 41761, 0.115999,),
    ("soc-sign-bitcoinotc.csv.gz", 5881, 21492, 0.068997, 856, 36894, 0.117996, 993, 48253, 0.145000,),
    ("soc-Slashdot0811.txt.gz", 77360, 546487, 3.708806, 7658, 12494, 0.0453784, 6334, 9138, 0.018000,),
    ("wiki-Vote.txt.gz", 7115, 100762, 0.794569, 766, 49995, 0.164172, 781, 48254, 0.144368,),
]

# Extracting the data
(dataset_names,
 nodes_1, edges_1, is_chordal_times,
 nodes_2, edges_2, chromatic_times,
 nodes_3, edges_3, independent_set_times) = zip(*datasets)


def plot_scatter_with_trendline(x, y, title, ylabel, filename):
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, label='Data Points')

    # Fit a linear trend line
    coeffs = np.polyfit(x, y, 1)
    trendline = np.polyval(coeffs, x)
    plt.plot(x, trendline, color='red', label='Trend Line')

    plt.xlabel('Sum of Nodes and Edges')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()


# Scatter plot for is_chordal with trend line
plot_scatter_with_trendline(edges_1, is_chordal_times,
                            'Execution Time for is_chordal Algorithm',
                            'Execution Time (seconds)',
                            'is_chordal_timing_graph.pdf')

# Scatter plot for chromatic_number_and_max_clique with trend line
plot_scatter_with_trendline(edges_2, chromatic_times,
                            'Execution Time for chromatic_number_and_max_clique Algorithm',
                            'Execution Time (seconds)',
                            'chromatic_number_and_max_clique_timing_graph.pdf')

# Scatter plot for max_independent_set_and_min_vertex_cover with trend line
plot_scatter_with_trendline(edges_3, independent_set_times,
                            'Execution Time for max_independent_set_and_min_vertex_cover Algorithm',
                            'Execution Time (seconds)',
                            'max_independent_set_and_min_vertex_cover_timing_graph.pdf')
