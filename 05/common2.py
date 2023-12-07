from __future__ import annotations

import re

class Range:
    start: int
    length: int
    end: int

    def __init__(self, start: int, length: int):
        self.start = start
        self.length = length
        self.end = start + length

class AlamanacRange:
    dest_range: Range
    src_range: Range

    def __init__(self, dest_start: int, source_start: int, length: int):
        self.dest_range = Range(dest_start, length)
        self.src_range = Range(source_start, length)

    def get_dest_range(self, val_range: Range) -> tuple[Range, Range]:
        if val_range.end <= self.src_range.start or self.src_range.end <= val_range.start:
            # No interception
            return Range(0, 0), Range(0, 0)
        elif val_range.start <= self.src_range.start and val_range.end >= self.src_range.end:
            # Whole self range fits
            return self.src_range, self.dest_range
        elif val_range.start >= self.src_range.start and val_range.end <=  self.src_range.end:
            # Whole val_range fits
            return val_range, Range(self.dest_range.start + val_range.start - self.src_range.start, val_range.length)
        elif val_range.end <= self.src_range.end:
            # val_range starts before self and ends before self
            return Range(self.src_range.start, val_range.end - self.src_range.start), Range(self.dest_range.start, val_range.end - self.src_range.start)
        elif val_range.start >= self.src_range.start:
            # val_range starts after self and sends after self
            return Range(val_range.start, self.src_range.end - val_range.start), Range(self.dest_range.start + val_range.start - self.src_range.start, self.src_range.end - val_range.start)


class AlamanacMap:
    src: str
    dest: str
    ranges: list[AlamanacRange]

    def __init__(self, src: str, dest: str, ranges: list[AlamanacRange]):
        self.src = src
        self.dest = dest
        self.ranges = ranges

    def get_dest_ranges(self, src_ranges: list[Range]) -> tuple[str, list[Range]]:
        return self.dest, self._get_dest_ranges(src_ranges)

    def _get_dest_ranges(self, src_ranges: list[Range]) -> list[Range]:
        dest_ranges_res: list[Range] = []
        for src_range in src_ranges:
            # Initial zero-len ranges just for filling in the gaps later
            src_ranges_mapped: list[Range] = [Range(src_range.start, 0), Range(src_range.end, 0)]
            dest_ranges: list[Range] = []
            for alamanac_range in self.ranges:
                src_range_mapped, dest_range = alamanac_range.get_dest_range(src_range)
                # zero-len ranges mean no interception
                if src_range_mapped.length > 0:
                    src_ranges_mapped.append(src_range_mapped)
                    dest_ranges.append(dest_range)
            # Fill in gaps in not mapped sources
            src_ranges_mapped.sort(key=lambda r: r.start)
            for i in range(len(src_ranges_mapped) - 1):
                if src_ranges_mapped[i + 1].start > src_ranges_mapped[i].end:
                    dest_ranges.append(Range(src_ranges_mapped[i].end, src_ranges_mapped[i + 1].start - src_ranges_mapped[i].end))
            dest_ranges_res.extend(dest_ranges)
        return dest_ranges_res


class Alamanac:
    seeds: list[int] | list[Range]
    maps: dict[str, AlamanacMap]

    def __init__(self, seeds: list[int] | list[Range], maps: dict[str, AlamanacMap]):
        self.seeds = seeds
        self.maps = maps

    def find_best_location_2(self):
        curr_name: str = "seed"
        curr_ranges: list[Range] = self.seeds
        while curr_name != "location":
            curr_name, curr_ranges = self.maps[curr_name].get_dest_ranges(curr_ranges)
        return min([r.start for r in curr_ranges])


map_pattern = '(?P<src>\w+)-to-(?P<dest>\w+) map'
map_vals_pattern = '(?P<dest_start>\d+)\s+(?P<src_start>\d+)\s+(?P<range_len>\d+)'


def parse_alamanac(lines: list[str], seeds: list[int] | list[Range]) -> Alamanac:
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
