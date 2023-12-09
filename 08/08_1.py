from utils.file_loader import load
from common import parse_nodes


def main():
    solution(load('08.txt'))


def solution(lines: list[str]):
    instructions: str = lines[0].replace('\n', '')
    nodes: dict[str, tuple[str, str]] = parse_nodes(lines)
    curr_node = 'AAA'
    i = 0
    while curr_node != 'ZZZ':
        curr_node = nodes[curr_node][0 if instructions[i % len(instructions)] == 'L' else 1]
        i += 1
    print(i)


main()
