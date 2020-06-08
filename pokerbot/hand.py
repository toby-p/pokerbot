
from collections import Counter

from card import Card
from variables import RANKS, ROYAL_RANKS, SUITS


ROYAL_FLUSHES = list()
for suit in SUITS:
    royal_flush = set([Card(f"{rank}{suit}") for rank in ROYAL_RANKS])
    ROYAL_FLUSHES.append(royal_flush)


class Hand:
    """Abstract class to construct a hand of unique card. Could be 2 cards,
    e.g. `hole` cards, or 5 cards, e.g. the hole cards plus the flop, etc."""

    def __init__(self, *cards):
        """A hand of playing cards."""
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

        # Save the cards and other important attributes for calculating hands:
        self.cards = sorted(parsed)
        self.ranks, self.int_ranks, self.suits, self.hashes = list(), list(), list(), list()
        self.longest_straight = 1
        self.longest_straight_high_card = None
        prev_rank, prev_suit, straight_count = -1, None, 1
        for c in self.cards:
            self.ranks.append(c.rank)
            self.int_ranks.append(int(c))
            self.suits.append(c.suit)
            self.hashes.append(hash(c))

            # Calculate longest straight, and highest card of the straight:
            int_rank = int(c)
            distance = int_rank - prev_rank
            if distance == 0:
                pass
            elif distance == 1:
                straight_count += 1
            else:
                straight_count = 1
            if straight_count >= self.longest_straight:
                self.longest_straight = straight_count
                self.longest_straight_high_card = c
            prev_rank = int_rank

        assert len(set(self.hashes)) == len(self.cards), "Duplicate playing cards in hand."
        self.n = len(self.cards)

        # Counts of attributes:
        rank_count = Counter(self.ranks)
        self.rank_count = {r: rank_count.get(r, 0) for r in RANKS}
        int_rank_count = Counter(self.int_ranks)
        self.int_rank_count = {i: int_rank_count.get(i, 0) for i in list(range(2, 15, 1))}
        suit_count = Counter(self.suits)
        self.suit_count = {s: suit_count.get(s, 0) for s in SUITS}

    @property
    def royal_flush(self):
        """Returns True if hand contains a royal flush, else False."""
        card_set = set(self.cards)
        for rf in ROYAL_FLUSHES:
            if rf.issubset(card_set):
                return True
        return False

    @property
    def straight_flush(self):
        """Returns True if hand contains a straight flush, else False."""
        if (self.longest_straight < 5) or (not self.flush_suits):
            return False
        # Iterate through suits checking for straight flushes:
        for s in self.flush_suits:
            cards = [c for c in self.cards if c.suit == s]
            prev_rank, sf_count = -1, 1
            for c in cards:
                int_rank = int(c)
                distance = int_rank - prev_rank
                if distance == 1:
                    sf_count += 1
                else:
                    sf_count = 1
                if sf_count == 5:
                    return True
                prev_rank = int_rank
        return False

    @property
    def flush_suits(self):
        """List of suits for which the hand holds a flush (i.e. >=5 cards)."""
        return [k for k, v in self.suit_count.items() if v >= 5]

    @property
    def full_house(self):
        """Returns True if hand contains a full house, else False."""
        threes, pairs = 0, 0
        for k, v in self.rank_count.items():
            if v >= 3:
                threes += 1
            elif v == 2:
                pairs += 1
            if threes >= 2:
                return True
            elif threes >= 1 and pairs >= 1:
                return True
        return False

    @property
    def pairs(self):
        """List of ranks for which the hand holds a pair. Only classifies ranks
        as a pair if there are exactly 2 cards in the hand of that rank
        (i.e. 2 cards from 3 of a kind isn't counted as a pair)."""
        return [k for k, v in self.rank_count.items() if v == 2]

    @property
    def trips(self):
        """List of ranks for which the hand holds 3 of a kind. Only classifies
        3 cards as a trip if there are exactly 3 cards of that rank (i.e. 3 cards
        from 4 of a kind isn't counted as a trip)."""
        return [k for k, v in self.rank_count.items() if v == 3]

    @property
    def quads(self):
        """List of ranks for which the hand holds all 4 cards."""
        return [k for k, v in self.rank_count.items() if v == 4]

    @property
    def best_hand(self):
        if self.royal_flush:
            return "RF"  # Royal flush.
        elif self.straight_flush:
            return "SF"  # Straight flush.
        elif self.quads:
            return "4"  # Four of a kind.
        elif self.full_house:
            return "FH"  # Full house.
        elif self.flush_suits:
            return "F"  # Flush.
        elif self.longest_straight >= 5:
            return "S"  # Straight.
        elif self.trips:
            return "3"  # Three of a kind.
        elif len(self.pairs) == 2:
            return "2P"  # Two pairs.
        elif len(self.pairs) == 1:
            return "P"  # Pair.
        else:
            return "HC"  # High card.


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
