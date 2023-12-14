from utils.file_loader import load
import itertools
import functools
import re


def main():
    solution(load('12.txt'))


record_pattern = '(?P<str_format>[\.#\?]+)\s+(?P<int_format>[\d,]+)'


def solution(lines: list[str]):
    res: int = 0
    for line in lines:
        record_match = re.search(record_pattern, line)
        record_str: str = record_match.group('str_format')
        record_int: list[int] = [int(num) for num in record_match.group('int_format').split(',')]
        res += count_poss('?'.join(list(itertools.repeat(record_str, 5))), tuple(record_int * 5), -1)
    print(res)

@functools.lru_cache(99999999)
def count_poss(record_str: str, record_int, dmg_len: int) -> int:
    if len(record_str) == 0:
        if dmg_len > 0:
            if len(record_int) == 0 or dmg_len != record_int[0]:
                return 0
            record_int = record_int[1:]
        return 1 if len(record_int) == 0 else 0
    if record_str[0] == '#':
        if not record_int:
            return 0
        jump: int = 1
        while jump < len(record_str) and record_str[jump] == '#':
            jump += 1
        return count_poss(record_str[jump:], record_int, jump if dmg_len == -1 else dmg_len + jump)
    elif record_str[0] == '.':
        if dmg_len > 0:
            if len(record_int) == 0 or dmg_len != record_int[0]:
                return 0
            else:
                record_int = record_int[1:]
        jump: int = 1
        while jump < len(record_str) and record_str[jump] == '.':
            jump += 1
        return count_poss(record_str[jump:], record_int, -1)
    else:
        return count_poss('.' + record_str[1:], record_int, dmg_len) + count_poss('#' + record_str[1:], record_int, dmg_len)


main()
