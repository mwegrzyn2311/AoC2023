from utils.file_loader import load
from common import Card, parse_cards


def main():
    solution(load('04.txt'))


def solution(lines: list[str]):
    cards: list[Card] = parse_cards(lines)
    for i in range(len(cards)):
        curr_card: Card = cards[i]
        for j in range(curr_card.matches):
            idx = i + j + 1
            if idx < len(cards):
                cards[idx].instances += curr_card.instances

    print(sum([card.instances for card in cards]))

main()
