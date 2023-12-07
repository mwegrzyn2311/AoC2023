from utils.file_loader import load
from common import parse_games


def main():
    solution(load('02.txt'))


def solution(lines: list[str]):
    games = parse_games(lines)
    print(sum([i for i in games if games[i]['red'] <= 12 and games[i]['green'] <= 13 and games[i]['blue'] <= 14]))


main()
