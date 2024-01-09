from utils.file_loader import load
from common import parse_bricks, simulate_brick_falling, how_many_will_fall_sum


def main():
    solution(load('22.txt'))


def solution(lines: list[str]):
    print(how_many_will_fall_sum(simulate_brick_falling(parse_bricks(lines))))


if __name__ == '__main__':
    main()
