from utils.file_loader import load
from common import parse_games


def main():
    solution(load('02.txt'))


def solution(lines: list[str]):
    games = parse_games(lines)
    print(sum([games[i]['red'] * games[i]['green'] * games[i]['blue'] for i in games]))


main()
