from utils.file_loader import load
from common import parse_nums


def main():
    solution(load('09.txt'))


def solution(lines: list[str]):
    print(sum([sum([nums[-1] for nums in numbers]) for numbers in parse_nums(lines)]))


main()
