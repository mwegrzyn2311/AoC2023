from utils.file_loader import load
from common import Engine, Coord, parse_engine


def main():
    solution(load('03.txt'))


def solution(lines: list[str]):
    engine: Engine = parse_engine(lines)
    print(engine.part_numbers_sum)

main()
