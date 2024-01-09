from utils.file_loader import load
from common import hash_str


def main():
    solution(load('15.txt'))


def solution(lines: list[str]):
    print(sum([hash_str(step) for step in lines[0].split(",")]))


if __name__ == '__main__':
    main()
