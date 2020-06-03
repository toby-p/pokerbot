"""Classes/functions for calculating odds at specific moments of a game."""

import os
import pandas as pd
import numpy as np

from deck import Deck
from card import Card

DIR, FILENAME = os.path.split(__file__)

ranks = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
suits = ("C", "D", "H", "S")


class HoldemFlopOdds:
    def __init__(self):
        fp = os.path.join(DIR, "indexes", "flop_index.csv")
        self.flop_index = pd.read_csv(fp, encoding="utf-8")
        self.odds_df = pd.DataFrame()

    def ix_hand(self, ix: int):
        """Inspect a hand by index of the `odds_df` DataFrame."""
        return sorted(self.odds_df.loc[ix, sorted(Deck.cards)].dropna().index)

    def create_hands_df(self, card1: Card, card2: Card):
        assert isinstance(card1, Card)
        assert isinstance(card2, Card)
        df = self.flop_index.copy()
        unseen = [c for c in Deck.cards if c not in (card1, card2)]
        columns = [c for c in sorted(unseen)]
        df.columns = columns
        df[card1], df[card2] = 1.0, 1.0
        card_columns = sorted(df.columns)

        # Sense check that all cards are accounted for:
        assert (len(df.columns) == 52) and (len(set(df.columns)) == 52)

        # Calculate the number of each suit in each hand:
        for suit in suits:
            suit_cols = [c for c in card_columns if c.suit == suit]
            df[suit] = df[suit_cols].sum(axis=1)
        # Calculate if hand contains a flush:
        df["suit_max"] = df[sorted(suits)].max(axis=1)
        df["flush"] = np.where(df["suit_max"] == 5, True, False)

        # Calculate the number of each rank in each hand, and highest/lowest rank:
        df["highest_rank"], df["lowest_rank"] = -1, 14
        for rank in ranks:
            rank_cols = [c for c in card_columns if c.rank == rank]
            df[rank] = df[rank_cols].sum(axis=1).astype(int)
            df["n_rank"] = np.where(df[rank], ranks.index(rank), np.nan)  # Rank as an integer.
            df["highest_rank"] = np.where(df["n_rank"] > df["highest_rank"], df["n_rank"], df["highest_rank"])
            df["lowest_rank"] = np.where(df["n_rank"] < df["lowest_rank"], df["n_rank"], df["lowest_rank"])
        rank_map = dict(enumerate(ranks))
        df["highest_rank"] = df["highest_rank"].map(rank_map)
        df["lowest_rank"] = df["lowest_rank"].map(rank_map)
        df.drop(columns=["n_rank"], inplace=True)

        # Calculate if hand contains pair/ 3/4 of a kind:
        for i, label in {2: "pair", 3: "three", 4: "four"}.items():
            boolean = df[sorted(ranks)] == i
            columns = [f"{label}_{r}" for r in sorted(ranks)]
            boolean.columns = columns
            boolean[f"{label}_count"] = boolean.sum(axis=1)
            df = df.merge(boolean, left_index=True, right_index=True)

        # Calculate if hand contains full house:
        df["full_house"] = (df["pair_count"] == 1) & (df["three_count"] == 1)

        # Save DataFrame:
        self.odds_df = df


def base_out_probability(n: int, to_deal: int, in_hand: int = 2,
                         on_table: int = 0, in_deck: int = 52):
    """Basic calculator for determining chance of hitting a certain number of
    cards with some number left to be dealt. E.g. if holding a pair and wanting
    to know probability of hitting a third pre-flop, `n`=2 (because there are 2
    possible cards in the deck which can result in 3 of a kind), and `to_deal`=5
    (because there are 5 cards left to be dealt).

    Args:
        n (int): the number of target cards left in the deck.
        to_deal (int): number of cards still to be dealt.
        in_hand (int): number of seen cards in your hand.
        on_table (int): number of seen cards on the table.
        in_deck (int): total number of cards in the deck.
    """
    not_probability = 1
    unseen_cards = in_deck - (in_hand + on_table)
    for _ in range(to_deal):
        not_dealt = (unseen_cards - n) / unseen_cards
        not_probability = not_probability * not_dealt
        unseen_cards -= 1
    return 1 - not_probability
