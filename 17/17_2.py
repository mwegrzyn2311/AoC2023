from utils.file_loader import load
from common import find_shortest_path_p2


def main():
    solution(load('17.txt'))


def solution(lines: list[str]):
    for y in range(len(lines)):
        lines[y] = lines[y].split('\n')[0]
    print(find_shortest_path_p2(lines))


if __name__ == '__main__':
    main()
