from utils.file_loader import load
from utils.common import Vector2
from common import transform_into_graph, longest_path


def main():
    solution(load('23.txt'))


def solution(lines: list[str]):
    start: Vector2 = Vector2(lines[0].index('.'), 0)
    last_row: int = len(lines) - 1
    end: Vector2 = Vector2(lines[last_row].index('.'), last_row)
    graph: dict[Vector2, set[tuple[Vector2, int]]] = transform_into_graph(lines, ignore_slopes=True)
    for node in graph:
        print(f'{node} -> {[pos for pos, dist in graph[node]]}')
    print(longest_path(graph, start, 0, [], end))


if __name__ == '__main__':
    main()
