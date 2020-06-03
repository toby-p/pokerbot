"""Script to set up files required by the package."""
from itertools import combinations
import numpy as np
import os
import pandas as pd


DIR, FILENAME = os.path.split(__file__)


def setup_dirs():
    indexes_fp = os.path.join(DIR, "indexes")
    if not os.path.exists(indexes_fp):
        os.mkdir(indexes_fp)


def setup_indexes():
    # Flop hands:
    flop_fp = os.path.join(DIR, "indexes", "flop_index.csv")
    if not os.path.exists(flop_fp):
        unseen = 50
        hands = list(combinations(list(range(unseen)), 3))
        df = pd.DataFrame([[1.0 if i in hand else np.nan for i in range(unseen)] for hand in hands])
        df.to_csv(flop_fp, encoding="utf-8", index=False)

    # Turn hands:
    turn_fp = os.path.join(DIR, "indexes", "turn_index.csv")
    if not os.path.exists(turn_fp):
        unseen = 47
        hands = list(combinations(list(range(unseen)), 1))
        df = pd.DataFrame([[1.0 if i in hand else np.nan for i in range(unseen)] for hand in hands])
        df.to_csv(turn_fp, encoding="utf-8", index=False)

    # River hands:
    river_fp = os.path.join(DIR, "indexes", "river_index.csv")
    if not os.path.exists(river_fp):
        unseen = 46
        hands = list(combinations(list(range(unseen)), 1))
        df = pd.DataFrame([[1.0 if i in hand else np.nan for i in range(unseen)] for hand in hands])
        df.to_csv(river_fp, encoding="utf-8", index=False)


if __name__ == "__main__":
    setup_dirs()
    setup_indexes()
