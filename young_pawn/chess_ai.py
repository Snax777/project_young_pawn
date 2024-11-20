"""
This AI will select chess moves that it sees fit for the current position.
"""

import random as r


def find_random_move(valid_moves):
    """
    Selects a valid move randomly.
    """
    return valid_moves[r.randint(0, len(valid_moves) - 1)]


def find_best_move():
    pass
