from utils.file_loader import load
from math import lcm
from common import parse_nodes


def main():
    solution(load('08.txt'))


def solution(lines: list[str]):
    instructions: str = lines[0].replace('\n', '')
    nodes: dict[str, tuple[str, str]] = parse_nodes(lines)
    curr_nodes: list[str] = [node for node in nodes if node[-1] == 'A']
    times_to_reach_goal: list[int] = []
    for curr_node in curr_nodes:
        i = 0
        while curr_node[-1] != 'Z':
            curr_node = nodes[curr_node][0 if instructions[i % len(instructions)] == 'L' else 1]
            i += 1
        times_to_reach_goal.append(i)
    print(lcm(*times_to_reach_goal))


main()
