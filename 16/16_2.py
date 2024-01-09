from utils.file_loader import load
from common import simulate_beams, Vector2


def main():
    solution(load('16.txt'))


def solution(lines: list[str]):
    for y in range(len(lines)):
        lines[y] = lines[y].split('\n')[0]

    max_res: int = -1
    for y in range(len(lines)):
        max_res = max(max_res, simulate_beams(lines, Vector2(0, y), Vector2(1, 0)), simulate_beams(lines, Vector2(len(lines[0]) - 1, y), Vector2(-1, 0)))
    for x in range(len(lines[0])):
        max_res = max(max_res, simulate_beams(lines, Vector2(x, 0), Vector2(0, 1)), simulate_beams(lines, Vector2(x, len(lines) - 1), Vector2(0, -1)))

    print(max_res)


if __name__ == '__main__':
    main()
