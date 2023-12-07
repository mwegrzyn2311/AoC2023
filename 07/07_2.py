from utils.file_loader import load
from functools import cmp_to_key
from common2 import CamelHand, parse_hands, compare_hands


def main():
    solution(load('07.txt'))


def solution(lines: list[str]):
    hands: list[CamelHand] = parse_hands(lines)
    hands.sort(key=cmp_to_key(compare_hands))
    print(sum([hand.bid * (i + 1) for i, hand in enumerate(hands)]))


main()
