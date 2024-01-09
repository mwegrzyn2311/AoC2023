from typing import Callable

import networkx as nx
import matplotlib.pyplot as plt


class GraphVisualization:

    def __init__(self):
        self.visual = []

    def add_edge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)

    def remove_edge(self, a, b):
        t1 = [a, b]
        if t1 in self.visual:
            self.visual.remove(t1)
        t2 = [b , a]
        if t2 in self.visual:
            self.visual.remove([b, a])

    def visualize(self):
        g = nx.Graph()
        g.add_edges_from(self.visual)
        nx.draw_networkx(g)
        plt.show()

    def visualize_directed(self):
        g = nx.DiGraph()
        g.add_edges_from(self.visual)
        nx.draw_networkx(g)
        plt.show()

    def visualize_custom(self, draw_fn: Callable[[nx.Graph], None]):
        g = nx.Graph()
        g.add_edges_from(self.visual)
        draw_fn(g)
        plt.show()
