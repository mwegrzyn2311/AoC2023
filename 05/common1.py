from __future__ import annotations

import re

class AlamanacRange:
    dest_start: int
    source_start: int
    length: int

    def __init__(self, dest_start: int, source_start: int, length: int):
        self.dest_start = dest_start
        self.source_start = source_start
        self.length = length

    def get_dest_value(self, value: int) -> int:
        return self.dest_start + (
                    value - self.source_start) if self.source_start <= value < self.source_start + self.length else -1

class AlamanacMap:
    src: str
    dest: str
    ranges: list[AlamanacRange]

    def __init__(self, src: str, dest: str, ranges: list[AlamanacRange]):
        self.src = src
        self.dest = dest
        self.ranges = ranges

    def get_dest(self, src_value: int) -> tuple[str, int]:
        return self.dest, self._get_dest_value(src_value)

    def _get_dest_value(self, src_value: int) -> int:
        for range in self.ranges:
            dest_value: int = range.get_dest_value(src_value)
            if dest_value > 0:
                return dest_value
        return src_value


class Alamanac:
    seeds: list[int]
    maps: dict[str, AlamanacMap]

    def __init__(self, seeds: list[int], maps: dict[str, AlamanacMap]):
        self.seeds = seeds
        self.maps = maps

    def find_best_location_1(self):
        return min([self.find_dest_value(seed, "seed", "location") for seed in self.seeds])

    def find_dest_value(self, start_val: int, start_name: str, dest_name: str) -> int:
        curr_name: str = start_name
        curr_val: int = start_val
        while curr_name != dest_name:
            curr_name, curr_val = self.maps[curr_name].get_dest(curr_val)
        return curr_val


map_pattern = '(?P<src>\w+)-to-(?P<dest>\w+) map'
map_vals_pattern = '(?P<dest_start>\d+)\s+(?P<src_start>\d+)\s+(?P<range_len>\d+)'


def parse_alamanac(lines: list[str], seeds: list[int]) -> Alamanac:
    maps: dict[str, AlamanacMap] = {}
    i: int = 2
    while i < len(lines):
        map_match = re.search(map_pattern, lines[i])
        ranges: list[AlamanacRange] = []
        i += 1
        while i < len(lines) and not lines[i].isspace():
            map_vals_match = re.search(map_vals_pattern, lines[i])
            ranges.append(AlamanacRange(int(map_vals_match.group('dest_start')), int(map_vals_match.group('src_start')),
                                        int(map_vals_match.group('range_len'))))
            i += 1
        maps[map_match.group('src')] = AlamanacMap(map_match.group('src'), map_match.group('dest'), ranges)
        while i < len(lines) and lines[i].isspace():
            i += 1
    return Alamanac(seeds, maps)
