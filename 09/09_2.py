from utils.file_loader import load
from common import parse_nums


def main():
    solution(load('09.txt'))


def solution(lines: list[str]):
    numbers_list: list[list[list[int]]] = parse_nums(lines)
    res: int = 0
    for numbers in numbers_list:
        numbers[-1].insert(0, numbers[-1][0])
        for i in range(len(numbers) - 2, -1, -1):
            numbers[i].insert(0, numbers[i][0] - numbers[i + 1][0])
        res += numbers[0][0]
    print(res)


main()
