from utils.file_loader import load
from common import shortest_paths_sum


def main():
    solution(load('11.txt'))


def solution(lines: list[str]):
    print(shortest_paths_sum(lines, 1000000))


main()
