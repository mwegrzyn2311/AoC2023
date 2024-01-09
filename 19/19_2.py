from utils.file_loader import load
from common2 import Workflow
from functools import reduce
from common2_v3 import Ranges, split_ranges


def main():
    solution(load('19.txt'))


def solution(lines: list[str]):
    i: int = 0
    while lines[i] != '\n':
        Workflow(lines[i])
        i += 1

    i += 1

    ranges: dict[str, list[tuple[int, int]]] = {'x': [(0, 4000)], 'm': [(0, 4000)], 'a': [(0, 4000)], 's': [(0, 4000)]}
    res: list[dict[str, list[tuple[int, int]]]] = Workflow.workflows['in'].apply(ranges)
    r: Ranges = {(0, 4000): {(0, 4000): {(0, 4000): {(0, 4000): 1}}}}
    print(split_ranges(r, 's', 2500, '>'))
    #print(combinations(list(res.values())))


def combinations(res_ranges: dict[str, [list[tuple[int, int]]]]) -> int:
    return reduce(lambda x, y: x * y, [sum([a_range[1] - a_range[0] + 1 for a_range in ranges]) for ranges in list(res_ranges.values())], 1)

if __name__ == '__main__':
    main()
