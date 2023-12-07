from utils.file_loader import load
from common import Engine, Coord, parse_engine


def main():
    solution(load('03.txt'))


def solution(lines: list[str]):
    engine: Engine = parse_engine(lines)
    print(sum([engine.gear_neighbours[gear_coord][0] * engine.gear_neighbours[gear_coord][1] for gear_coord in engine.gear_neighbours if len(engine.gear_neighbours[gear_coord]) == 2]))

main()
