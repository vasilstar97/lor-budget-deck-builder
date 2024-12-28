from .card import Card
from .rarity import Rarity
from ..parser import parser

class Deck():

    def __init__(self, cards : dict[str, int] | dict[Card, int]):
        self.cards = {Card(card) if isinstance(card, str) else Card(card.code) : count for card, count in cards.items()}

    @property
    def cost(self):
        return sum([count * card.rarity for card, count in self.cards.items()])

    @classmethod
    def sample(cls):
        ...

    @classmethod
    def from_list(cls, cards_list : list[str]):
        cards_dict = {Card(card) : cards_list.count(card) for card in set(cards_list)}
        return cls(cards_dict)

    @classmethod
    def from_code(cls, code : str):
        cards = parser.get_cards_from_code(code)
        return cls.from_list(cards)
    
    def __len__(self) -> int:
        return sum(self.cards.values(), 0)

    def __add__(self, other):
        if isinstance(other, Deck):
            deck_a = self.cards.copy()
            deck_b = other.cards.copy()
            deck_c = {}

            for card in {*deck_a.keys(), *deck_b.keys()}:
                count_a = deck_a[card] if card in deck_a else 0
                count_b = deck_b[card] if card in deck_b else 0
                deck_c[card] = min(3, count_a + count_b)
            
            return Deck(deck_c)
        else:
            raise TypeError('Cant make sum')

    def __sub__(self, other):
        if isinstance(other, Deck):
            deck_a = self.cards.copy()
            deck_b = other.cards.copy()
            deck_c = {}
            for card, count_a in deck_a.items():
                count_b = deck_b.get(card, 0)
                count_c = count_a - count_b
                if count_c > 0:
                    deck_c[card.code] = count_c    
            return Deck(deck_c)
        else:
            raise TypeError('Cant make difference')
        
    def __repr__(self) -> str:
        champions = {card for card in self.cards if card.rarity == Rarity.CHAMPION}
        return str.join(', ', [card.name for card in champions])