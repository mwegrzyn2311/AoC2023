import re
from typing import Callable
from copy import deepcopy

workflow_pattern: re.Pattern = re.compile('(?P<workflow_name>\w+){(?P<conditions>.+)}')
condition_pattern: re.Pattern = re.compile('(?P<category>\w+)(?P<operator>[<>])(?P<value>\d+):(?P<result>\w+)')

empty_ranges: dict[tuple[int, int], dict[tuple[int, int], dict[tuple[int, int], tuple[int, int]]]] = {(0, 4000): {(0, 4000): {(0, 4000): (0, 4000)}}}
ranges: dict[tuple[int, int], dict[tuple[int, int], dict[tuple[int, int], tuple[int, int]]]] = {
    (10, 40): {
        (1, 13): {

        },
        (14,66)
    },
    (41, 50)
}

def merge_ranges(ranges1: dict[str, list[tuple[int, int]]], ranges2: dict[str, list[tuple[int, int]]]) -> dict[str, list[tuple[int, int]]]:
    return {
        'x': merge_tuples(ranges1['x'], ranges2['x']),
        'm': merge_tuples(ranges1['m'], ranges2['m']),
        'a': merge_tuples(ranges1['a'], ranges2['a']),
        's': merge_tuples(ranges1['s'], ranges2['s'])
    }


def merge_tuples(t1: list[tuple[int, int]], t2: list[tuple[int, int]]) -> list[tuple[int, int]]:
    # sort
    t1.sort(key=lambda x: x[0])
    t2.sort(key=lambda x: x[0])
    print(t1)
    print(t2)
    print("-----")

    # insert
    res: list[tuple[int, int]] = []
    i1: int = 0
    i2: int = 0
    while i1 < len(t1) and i2 < len(t2):
        if t2[i2][0] <= t1[i1][0]:
            start = t2[i2][0]
            curr_end = t2[i2][1]
            # print(f'1 - {start} - {curr_end} - {i1} - {i2}')
            i2 += 1
        else:
            start = t1[i1][0]
            curr_end = t1[i1][1]
            i1 += 1
        while (i2 < len(t2) and curr_end >= t2[i2][0] - 1) or (i1 < len(t1) and curr_end >= t1[i1][0] - 1):
            if i2 < len(t2) and curr_end >= t2[i2][0] - 1:
                curr_end = max(curr_end, t2[i2][1])
                i2 += 1
            if i1 < len(t1) and curr_end >= t1[i1][0] - 1:
                curr_end = max(curr_end, t1[i1][1])
                i1 += 1
        res.append((start, curr_end))
    print(res + t1[i1:] + t2[i2:])
    print("======")
    return res + t1[i1:] + t2[i2:]


def split_ranges(ranges: dict[str, list[tuple[int, int]]], split_cat: str, split_val: int, split_char: str) -> tuple[dict[str, list[tuple[int, int]]], dict[str, list[tuple[int, int]]]]:
    border_value = split_val + (1 if split_char == '>' else -1)
    for range in ranges[split_cat]:
        if range[0] <= border_value <= range[1]:
            new_ranges1 = deepcopy(ranges)
            new_ranges2 = deepcopy(ranges)
            new_ranges1[split_cat].remove(range)
            new_ranges2[split_cat].remove(range)
            if split_char == '>':
                new_ranges1[split_cat].append((border_value, range[1]))
                new_ranges2[split_cat].append((range[0], border_value - 1)) # split_val
            elif split_char == '<':
                new_ranges1[split_cat].append((range[0], border_value)) # split_val - 1
                new_ranges2[split_cat].append((border_value + 1, range[1]))
            else:
                print("ERR")
            return new_ranges1, new_ranges2
    return {}, {}


class Workflow:
    name: str
    conditions: list[Callable[[dict[str, list[tuple[int, int]]], int], dict[str, list[tuple[int, int]]]]]
    # static
    workflows: dict = {}

    def __init__(self, workflow_str: str):
        workflow_match: re.Match = workflow_pattern.search(workflow_str)
        self.name = workflow_match.group('workflow_name')
        self.conditions = [self.__parse_condition(condition_str) for condition_str in workflow_match.group('conditions').split(',')]
        Workflow.workflows[self.name] = self

    def __parse_condition(self, condition_str: str) -> Callable[[dict[str, list[tuple[int, int]]], int], dict[str, list[tuple[int, int]]]]:
        condition_match: re.Match = condition_pattern.search(condition_str)
        if condition_match:
            result = condition_match.group('result')
            return lambda ranges, i: merge_ranges(split_ranges(ranges, condition_match.group('category'), int(condition_match.group('value')), condition_match.group('operator'))[0] if result == 'A' else empty_ranges if result == 'R' else Workflow.workflows[result].apply(split_ranges(ranges, condition_match.group('category'), int(condition_match.group('value')), condition_match.group('operator'))[0]), self.conditions[i + 1](split_ranges(ranges, condition_match.group('category'), int(condition_match.group('value')), condition_match.group('operator'))[1], i + 1))
        else:
            return lambda ranges, i: ranges if condition_str == 'A' else empty_ranges if condition_str == 'R' else Workflow.workflows[condition_str].apply(ranges)

    def apply(self, ranges: dict[str, list[tuple[int, int]]]) -> dict[str, list[tuple[int, int]]]:
        return self.conditions[0](ranges, 0)
