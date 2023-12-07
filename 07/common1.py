from enum import IntEnum


class HandType(IntEnum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE = 4
    FULL = 5
    FOUR = 6
    FIVE = 7


class CamelHand:
    cards: list[int]
    bid: int
    type: HandType

    def __init__(self, cards: list[int], bid: int):
        self.cards = cards
        self.bid = bid
        self.type = self.__determine_type()

    def __determine_type(self) -> HandType:
        unique_cards: dict[int, int] = {}
        for card in self.cards:
            unique_cards[card] = 1 if card not in unique_cards else unique_cards[card] + 1
        unique_cards_nums: list[int] = list(unique_cards.values())
        if len(unique_cards_nums) == 1:
            return HandType.FIVE
        elif len(unique_cards_nums) == 2:
            return HandType.FOUR if max(unique_cards_nums) == 4 else HandType.FULL
        elif len(unique_cards_nums) == 3:
            return HandType.THREE if max(unique_cards_nums) == 3 else HandType.TWO_PAIR
        elif len(unique_cards_nums) == 4:
            return HandType.PAIR
        else:
            return HandType.HIGH_CARD


def compare_hands(hand1: CamelHand, hand2: CamelHand) -> int:
    if hand1.type == hand2.type:
        for i in range(5):
            if hand1.cards[i] != hand2.cards[i]:
                return hand1.cards[i] - hand2.cards[i]
        print("Equality")
        return 0
    else:
        return hand1.type - hand2.type


CARD_TO_VALUE: dict[str, int] = {
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}


def get_card_value(card: str) -> int:
    return CARD_TO_VALUE[card] if card in CARD_TO_VALUE else int(card)


def parse_hands(lines: list[str]) -> list[CamelHand]:
    res: list[CamelHand] = []
    for line in lines:
        line_split: list[str] = line.split()
        res.append(CamelHand([get_card_value(v) for i, v in enumerate(line_split[0])], int(line_split[1])))
    return res
