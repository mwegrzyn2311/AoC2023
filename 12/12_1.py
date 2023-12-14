from utils.file_loader import load
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
        res += pow(count_poss(record_str, record_int, 0), 5)
    print(res)


def count_poss(record_str: str, record_int: list[int], idx: int) -> int:
    if idx == len(record_str):
        return 1 if records_match(record_str, record_int) else 0
    if record_str[idx] != '?':
        return count_poss(record_str, record_int, idx + 1)
    return (count_poss(record_str[:idx] + '.' + record_str[idx + 1:], record_int, idx + 1)
            + count_poss(record_str[:idx] + '#' + record_str[idx + 1 :], record_int, idx + 1))


def records_match(record_str: str, record_int: list[int]) -> bool:
    i_str: int = 0
    i_list: int = 0
    while i_list < len(record_int):
        while i_str < len(record_str) and record_str[i_str] == '.':
            i_str += 1
        damaged_len: int = 0
        while i_str < len(record_str) and record_str[i_str] == '#':
            damaged_len += 1
            i_str += 1
        if damaged_len != record_int[i_list]:
            return False
        i_list += 1
    while i_str < len(record_str):
        if record_str[i_str] == '#':
            return False
        i_str += 1
    return True

main()
