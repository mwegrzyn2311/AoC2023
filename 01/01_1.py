from utils.file_loader import load


def main():
    solution(load('01.txt'))


def solution(lines: list[str]):
    print(sum([first_digit(line) * 10 + first_digit(line[::-1]) for line in lines]))


def first_digit(line: str) -> int:
    return int(next(x for x in line if x.isdigit()))


main()
