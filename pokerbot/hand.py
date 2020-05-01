
from collections import Counter

from card import Card


class TexasHoldem5Hand:
    """A hand of 5 cards in Texas Hold 'Em."""

    def __init__(self, *cards):
        """A hand of 5 playing cards."""
        assert len(cards) == 5, "Invalid number of cards passed, must be exactly 5."
        parsed = list()
        for c in cards:
            if isinstance(c, Card):
                parsed.append(c)
            elif isinstance(c, str):
                parsed.append(Card(c))
            elif isinstance(c, tuple):
                parsed.append(Card(*c))
            else:
                raise TypeError(f"Invalid type to interpret as a card: {type(c)}")
        self.__cards = sorted(parsed)
        ranks, suits, hashes = list(), list(), list()
        for c in self.cards:
            ranks.append(int(c))
            suits.append(c.suit)
            hashes.append(hash(c))
        assert len(set(hashes)) == len(cards), "Duplicate playing cards in hand."
        self.__ranks = ranks
        self.__suits = suits
        self.__suit_count = Counter(self.suits)
        self.__rank_count = Counter(self.ranks)

    @property
    def cards(self):
        return self.__cards

    @property
    def ranks(self):
        return self.__ranks

    @property
    def suits(self):
        return self.__suits

    @property
    def suit_count(self):
        return self.__suit_count

    @property
    def rank_count(self):
        return self.__rank_count

    @property
    def straight_high_card(self):
        """If the cards are a straight returns the rank of the highest card,
        else returns None."""
        r = self.ranks
        distances = [r[i] - r[i - 1] for i in range(1, 5, 1)]
        if set(distances) == {1}:
            return int(self.cards[-1])
        else:
            return

    @property
    def flush_suit(self):
        """If the hand is a flush (all the same suit), then returns the suit,
        else returns None."""
        if max(self.suit_count.values()) == 5:
            return list(self.suit_count.keys())[0]
        else:
            return

    @property
    def full_house(self):
        """If the cards are a full house return a tuple of the triple and the
        pair, else returns None."""
        if self.triple and self.pairs:
            return self.triple, self.pairs[0]
        else:
            return

    @property
    def best_hand(self):
        if self.straight_high_card == 14 and self.flush_suit:
            return "RF"  # Royal flush.
        elif self.straight_high_card and self.flush_suit:
            return "SF"  # Straight flush.
        elif self.quad:
            return "4"  # Four of a kind.
        elif self.full_house:
            return "FH"  # Full house.
        elif self.flush_suit:
            return "F"  # Flush.
        elif self.straight_high_card:
            return "S"  # Straight.
        elif self.triple:
            return "3"  # Three of a kind.
        elif len(self.pairs) == 2:
            return "2P"  # Two pairs.
        elif len(self.pairs) == 1:
            return "P"  # Pair.
        else:
            return "HC"  # High card.

    @property
    def pairs(self):
        """Return a tuple of each pair of cards in the hand. Only classifies 2
        cards as a pair if there are exactly 2 cards in the hand with that rank
        (i.e. 2 cards from 3 of a kind wouldn't be counted as a pair)."""
        ranks = [k for k, v in self.rank_count.items() if v == 2]
        pairs = list()
        for r in ranks:
            p = [c for c in self.cards if int(c) == r]
            pairs.append(tuple(p))
        return tuple(pairs)

    @property
    def triple(self):
        """Return a tuple of the 3 cards that make up a triple of cards with the
        same rank. Only classifies 3 cards as a triple if there are exactly 3
        cards in the hand with that rank (i.e. 3 cards from 4 of a kind wouldn't
        be counted as a triple)."""
        ranks = [k for k, v in self.rank_count.items() if v == 3]
        if ranks:
            return tuple([c for c in self.cards if int(c) == ranks[0]])
        else:
            return

    @property
    def quad(self):
        """Return a tuple of the 4 cards that make up a 4 of a kind with the
        same rank."""
        ranks = [k for k, v in self.rank_count.items() if v == 4]
        if ranks:
            return tuple([c for c in self.cards if int(c) == ranks[0]])
        else:
            return

    @property
    def kickers(self):
        """For hands with spare cards (single pair, 2 pairs, 3 of a kind, high
        card), return a sorted list of the kickers."""
        hand = self.best_hand
        if hand in ("P", "2P"):
            cards = [c for t in self.pairs for c in t]
            kickers = [c for c in self.cards if c not in cards][::-1]
        elif hand == "3":
            kickers = [c for c in self.cards if c not in self.triple][::-1]
        elif hand == "HC":
            kickers = self.cards[:-1][::-1]
        else:
            kickers = tuple()
        return tuple(kickers)
