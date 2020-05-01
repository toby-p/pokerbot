
from itertools import product
import random


from card import Card


class Deck:
    """A single standard deck of 52 playing cards."""

    def __init__(self):
        ranks = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
        suits = ("C", "D", "H", "S")
        self.__dealt = list()
        self.__cards = [Card(t[0], t[1]) for t in list(product(suits, ranks))]
        self.shuffle()

    @property
    def cards(self):
        return self.__cards

    @property
    def dealt(self):
        return self.__dealt

    @property
    def not_dealt(self):
        return self.__not_dealt

    def deal(self):
        """Deal a card."""
        try:
            card = self.not_dealt.pop(0)
            self.__dealt.append(card)
            return card
        except IndexError:
            raise IndexError("All cards in deck dealt.")

    def shuffle(self):
        """Shuffle the deck at the `cards` attribute."""
        assert not len(self.dealt), "Cannot shuffle cards after dealing starts."
        random.shuffle(self.cards)
        self.__not_dealt = self.cards.copy()
