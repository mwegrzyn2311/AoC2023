import re
from utils.file_loader import load
from common1 import parse_alamanac


def main():
    solution(load('05.txt'))


seeds_pattern = 'seeds:\s+(?P<seeds>.*)'


def solution(lines: list[str]):
    print(parse_alamanac(lines, [int(seed) for seed in
                                 re.search(seeds_pattern, lines[0]).group('seeds').split()]).find_best_location_1())


main()
