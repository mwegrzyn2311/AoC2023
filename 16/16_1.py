from utils.file_loader import load
from common import simulate_beams, Vector2


def main():
    solution(load('16.txt'))


def solution(lines: list[str]):
    for y in range(len(lines)):
        lines[y] = lines[y].split('\n')[0]

    print(simulate_beams(lines, Vector2(3, 0), Vector2(0, 1)))


if __name__ == '__main__':
    main()
