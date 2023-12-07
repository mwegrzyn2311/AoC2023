from utils.file_loader import load
from common import Card, parse_cards

def main():
    solution(load('04.txt'))


def solution(lines: list[str]):
    cards: list[Card] = parse_cards(lines)
    print(sum(card.value() for card in cards))

main()
