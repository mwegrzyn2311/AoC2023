from utils.graph import GraphVisualization


class Graph:
    nodes: dict[str, list[str]]
    wires: list[tuple[str, str]]

    def __init__(self):
        self.nodes = {}
        self.wires = []

    def add_node(self, node: str, connected: list[str]):
        if node not in self.nodes:
            self.nodes[node] = []
        for n in connected:
            self.nodes[node].append(n)
            self.wires.append((node, n))
            if n not in self.nodes:
                self.nodes[n] = [node]
            else:
                self.nodes[n].append(node)

    def remove_edge(self, n1: str, n2: str):
        self.nodes[n1].remove(n2)
        self.nodes[n2].remove(n1)


def parse_graph(lines: list[str]) -> Graph:
    graph = Graph()
    g_viz = GraphVisualization()
    for line in lines:
        node_parts: list[str] = line.split(': ')
        graph.add_node(node_parts[0], node_parts[1].split())
        for b in node_parts[1].split():
            g_viz.add_edge(node_parts[0], b)
    graph.remove_edge('jxm', 'qns')
    g_viz.remove_edge('jxm', 'qns')
    graph.remove_edge('dbt', 'tjd')
    g_viz.remove_edge('dbt', 'tjd')
    graph.remove_edge('plt', 'mgb')
    g_viz.remove_edge('plt', 'mgb')
    g_viz.visualize()
    return graph


def rec(nodes: dict[str, list[str]], curr_node: str, visited: dict[str, bool]):
    if visited[curr_node]:
        return
    visited[curr_node] = True
    for neighbor in nodes[curr_node]:
        rec(nodes, neighbor, visited)


def conn_nodes_size(nodes: dict[str, list[str]]) -> int:
    visited: dict[str, bool] = {node: False for node in nodes.keys()}
    for node, _ in nodes.items():
        rec(nodes, node, visited)
        return len([1 for is_visited in visited.values() if is_visited])
