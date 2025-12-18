# PART 1
# INSTRUCTIONS

# EXAMPLE

# PART 2

# INSTRUCTIONS

# EXAMPLE

from .base_solver import solver
import networkx as nx
from tqdm import tqdm
import matplotlib.pyplot as plt
import threading
from functools import cache

# solver class has a self.parser to read the file for the day.
def build_graph(data) -> nx.Graph:
    G = nx.DiGraph()
    for line in data:
        input, outputs = line[0][:-1], line[1:]
        for output in outputs:
            G.add_edge(input, output)
    return G

def draw_graph(G):
    # draw the graph in a new thread?    
    plt.figure(figsize=(12, 8)) 
    nx.draw(G, with_labels=True)
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    plt.show()

def count_paths_dp(G:nx.Graph, topo_order, start, end):
    # Initialize memoization dictionary
    paths_to_node = {node: 0 for node in G.nodes()}
    paths_to_node[start] = 1
    
    # Process nodes in topological order
    for node in topo_order:
        if paths_to_node[node] > 0:  # If this node is reachable
            for successor in G.successors(node):
                paths_to_node[successor] += paths_to_node[node]
    
    return paths_to_node[end]

class solve(solver):
    def part1(self):
        data = self.parser.file_to_matrix_sep(' ')
        G = build_graph(data)
        res = len(list(nx.all_simple_paths(G, "you", "out")))
        return res
    
    def part2(self):
        data = self.parser.file_to_matrix_sep(' ')
        G = build_graph(data)
        # threading.Thread(target=draw_graph, args=(G,)).start()
        topo_order = list(nx.topological_sort(G))
        
        a = count_paths_dp(G, topo_order, "svr", "fft")
        b = count_paths_dp(G, topo_order, "fft", "dac")
        c = count_paths_dp(G, topo_order, "dac", "out")
        
        return a * b * c