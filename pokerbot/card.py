

class Card:
    """A single playing card."""

    def __init__(self, *args):
        """Create an instance to store the value of a single playing card. Suit
        and rank can either be passed as 2 separate arguments, or as a single
        string, e.g. `as` for Ace of Spades, `d10` for 10 of Diamonds, etc.
        """
        if len(args) == 1:
            card = args[0]
            if str(card[-1]).upper() in list("CDHS"):
                rank, suit = card[:-1], card[-1]
            elif str(card[0]).upper() in list("CDHS"):
                suit, rank = card[0], card[1:]
            else:
                raise ValueError(f"Couldn't parse suit and rank from: {card}")
        elif len(args) == 2:
            if str(args[0]).upper() in list("CDHS"):
                rank, suit = args[1], args[0]
            elif str(args[1]).upper() in list("CDHS"):
                rank, suit = args[0], args[1]
            else:
                raise ValueError(f"Couldn't parse suit and rank from: {args}")
        else:
            raise ValueError(f"Couldn't parse suit and rank from: {args}")
        self.__rank = self.parse_rank(rank)
        self.__suit = self.parse_suit(suit)

    @property
    def rank(self):
        return self.__rank

    @property
    def suit(self):
        return self.__suit

    @staticmethod
    def parse_rank(rank):
        try:  # Rank passed as integer:
            parsed_rank = int(rank)
            assert parsed_rank in range(1, 14, 1), f"Invalid card rank (must be in range 1 <= 13): {rank}"
            parsed_rank = str(parsed_rank)
            parsed_rank = {"1": "A", "11": "J", "12": "Q", "13": "K"}.get(parsed_rank, parsed_rank)
        except ValueError:  # Assume rank passed as str:
            parsed_rank = str.upper(rank)[0]
            assert parsed_rank in list("JQKA"), f"Invalid card rank: {rank}"
        return parsed_rank

    @staticmethod
    def parse_suit(suit: str):
        parsed_suit = str.upper(suit[0])
        assert parsed_suit in list("CDHS"), f"Invalid suit: {suit}"  # Clubs, Diamonds, Hearts, Spades.
        return parsed_suit

    def __hash__(self):
        suit = {"C": 0, "D": 1, "H": 2, "S": 3}[self.suit] * 14
        return suit + int(self)

    def __repr__(self):
        return f"{self.rank}{self.suit}"

    def __int__(self):
        return int({"J": 11, "Q": 12, "K": 13, "A": 14}.get(self.rank, self.rank))

    def __str__(self):
        rank = {"J": "Jack", "Q": "Queen", "K": "King", "A": "Ace"}.get(self.rank, self.rank)
        suit = {"C": "Clubs", "D": "Diamonds", "H": "Hearts", "S": "Spades"}.get(self.suit)
        return f"{rank} of {suit}"

    def __eq__(self, other):
        """Returns True only if the rank and suit of the cards both match."""
        return True if ((self.rank == other.rank) and (self.suit == other.suit)) else False

    def __ne__(self, other):
        """Returns False if the rank or suit of this card differs from other."""
        return True if ((self.rank != other.rank) or (self.suit != other.suit)) else False

    def __lt__(self, other):
        return True if (int(self) < int(other)) else False

    def __gt__(self, other):
        return True if (int(self) > int(other)) else False

    def __le__(self, other):
        return True if (int(self) <= int(other)) else False

    def __ge__(self, other):
        return True if (int(self) >= int(other)) else False
