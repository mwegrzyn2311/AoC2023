from __future__ import annotations

import re
from typing import Callable
from copy import deepcopy

workflow_pattern: re.Pattern = re.compile('(?P<workflow_name>\w+){(?P<conditions>.+)}')
condition_pattern: re.Pattern = re.compile('(?P<category>\w+)(?P<operator>[<>])(?P<value>\d+):(?P<result>\w+)')

Ranges = dict[tuple[int, int], dict[tuple[int, int], dict[tuple[int, int], dict[tuple[int, int]], 1]]]
empty_ranges: Ranges = {}


def merge_r_dicts(d1: dict, d2: dict) -> dict:


def merge_ranges(ranges1: Ranges, ranges2: Ranges) -> Ranges:
    if ranges1 == empty_ranges:
        return ranges2
    if ranges2 == empty_ranges:
        return ranges1




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


iters: dict[str, int] = {
    'x': 0,
    'm': 1,
    'a': 2,
    's': 3
}


def find_key(d: dict, split_val: int) -> tuple[int, int] | None:
    for key in d.keys():
        if key[0] <= split_val <= key[1]:
            return key
    return None


def split_ranges(ranges: Ranges, split_cat: str, split_val: int, split_char: str) -> tuple[Ranges, Ranges]:
    border_value = split_val if split_char == '>' else split_val - 1
    ranges1: Ranges = deepcopy(ranges)
    ranges2: Ranges = deepcopy(ranges)
    to_modify1: list[dict] = [ranges1]
    to_modify2: list[dict] = [ranges2]
    for i in range(iters[split_cat]):
        new_to_modify1: list[dict] = []
        new_to_modify2: list[dict] = []
        for d in to_modify1:
            new_to_modify1 += d.values()
        for d in to_modify2:
            new_to_modify2 += d.values()
        to_modify1 = new_to_modify1
        to_modify2 = new_to_modify2

    for i in range(len(to_modify1)):
        key: tuple[int, int] | None = find_key(to_modify1[i], split_val)
        if key is not None:
            k1: tuple[int, int] = (key[0], split_val)
            k2: tuple[int, int] = (split_val + 1, key[1])
            v1 = to_modify1[i][key]
            v2 = to_modify2[i][key]
            del to_modify1[i][key]
            to_modify1[i][k1] = v1
            del to_modify2[i][key]
            to_modify2[i][k2] = v2

    if split_char == '<':
        return ranges1, ranges2
    elif split_char == '>':
        return ranges2, ranges1
    return {}, {}


class Workflow:
    name: str
    conditions: list[Callable[[Ranges, int], Ranges]]
    # static
    workflows: dict = {}

    def __init__(self, workflow_str: str):
        workflow_match: re.Match = workflow_pattern.search(workflow_str)
        self.name = workflow_match.group('workflow_name')
        self.conditions = [self.__parse_condition(condition_str) for condition_str in workflow_match.group('conditions').split(',')]
        Workflow.workflows[self.name] = self

    def __parse_condition(self, condition_str: str) -> Callable[[Ranges, int], Ranges]:
        condition_match: re.Match = condition_pattern.search(condition_str)
        if condition_match:
            result = condition_match.group('result')
            return lambda ranges, i: merge_ranges(split_ranges(ranges, condition_match.group('category'), int(condition_match.group('value')), condition_match.group('operator'))[0] if result == 'A' else empty_ranges if result == 'R' else Workflow.workflows[result].apply(split_ranges(ranges, condition_match.group('category'), int(condition_match.group('value')), condition_match.group('operator'))[0]), self.conditions[i + 1](split_ranges(ranges, condition_match.group('category'), int(condition_match.group('value')), condition_match.group('operator'))[1], i + 1))
        else:
            return lambda ranges, i: ranges if condition_str == 'A' else empty_ranges if condition_str == 'R' else Workflow.workflows[condition_str].apply(ranges)

    def apply(self, ranges: Ranges) -> Ranges:
        return self.conditions[0](ranges, 0)
