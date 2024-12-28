from ..parser import parser
from .rarity import Rarity

CARDS_RARITIES = parser.get_cards_rarities()
CARDS_NAMES = parser.get_cards_names()

class Card():
    
    def __init__(self, code : str):
        self.code = code

    @property
    def rarity(self) -> Rarity:
        return CARDS_RARITIES[self.code]
    
    @property
    def name(self) -> str:
        return CARDS_NAMES[self.code]

    def __eq__(self, other) -> bool:
        if isinstance(other, Card):
            return self.code == other.code
        else:
            raise TypeError('Cant compare card with something else')
        
    def __hash__(self) -> int:
        return hash(self.code)
    
    def __repr__(self) -> str:
        return self.name