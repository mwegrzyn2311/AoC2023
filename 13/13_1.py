from utils.file_loader import load
from common import parse_mirrors, mirror_value


def main():
    solution(load('13.txt'))


def solution(lines: list[str]):
    mirrors: list[list[str]] = parse_mirrors(lines)

    print(sum(mirror_value(mirror) for mirror in mirrors))


main()
