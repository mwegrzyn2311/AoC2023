from utils.file_loader import load
from common import Graph, parse_graph, conn_nodes_size
import sys


def main():
    solution(load('25.txt'))


def solution(lines: list[str]):
    graph: Graph = parse_graph(lines)
    for node in graph.nodes:
        print(f'{node} -> {graph.nodes[node]}')
    size1: int = conn_nodes_size(graph.nodes)
    print(size1 * (len(graph.nodes) - size1))


if __name__ == '__main__':
    main()
