import re


class Card:
    winning: list[int]
    owned: list[int]
    matches: int
    instances: int

    def __init__(self, winning: list[int], owned: list[int]):
        self.winning = winning
        self.owned = owned
        self.matches = len([num for num in self.winning if num in self.owned])
        self.instances = 1

    def value(self):
        return pow(2, self.matches - 1) if self.matches - 1 >= 0 else 0


card_pattern = 'Card\s+\d+:\s+(?P<winning>.*)\s+\|\s+(?P<owned>.*)'


def parse_cards(lines: list[str]) -> list[Card]:
    cards: list[Card] = []
    for line in lines:
        card_match = re.search(card_pattern, line)
        cards.append(Card(parse_ints(card_match, 'winning'), parse_ints(card_match, 'owned')))
    return cards


def parse_ints(match: re.Match, group_name: str) -> list[int]:
    return [int(number) for number in match.group(group_name).split()]
