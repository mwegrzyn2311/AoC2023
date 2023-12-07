import re
from utils.file_loader import load
from common2 import parse_alamanac, Range


def main():
    solution(load('05.txt'))


seeds_pattern = 'seeds:\s+(?P<seeds>.*)'


def solution(lines: list[str]):
    seeds_str: list[str] = re.search(seeds_pattern, lines[0]).group('seeds').split()
    seeds: list[Range] = []
    for i in range(0, len(seeds_str), 2):
        seeds.append(Range(int(seeds_str[i]), int(seeds_str[i + 1])))
    print(parse_alamanac(lines, seeds).find_best_location_2())


main()
