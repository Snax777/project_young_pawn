"""
This AI will select chess moves that it sees fit for the current position.
"""

import random as r


piece_value = {
    "K": 100,
    "Q": 9,
    "R": 5,
    "B": 3,
    "N": 3,
    "p": 1,
}
CHECKMATE = 1000
STALEMATE = 0


def find_random_move(valid_moves):
    """
    Selects a valid move randomly.
    """
    return valid_moves[r.randint(0, len(valid_moves) - 1)]


def score_material(board):
    """
    Scores White and Black based on the remaining materials each side has.
    """
    score = 0

    for row in board:
        for square in row:
            if square[0] == "w":
                score += piece_value[square[1]]
            elif square[0] == "b":
                score -= piece_value[square[1]]

    return score


def find_greedy_move(game_state, valid_moves):
    """
    Selects move based on current possible piece captures.
    """
    turn = 1 if game_state.white_to_move else -1
    opp_minmax_score = CHECKMATE
    best_player_move = None

    r.shuffle(valid_moves)

    for player_move in valid_moves:
        game_state.make_move(player_move)

        opp_moves = game_state.get_valid_moves()
        opp_max_score = -CHECKMATE

        for opp_move in opp_moves:
            game_state.make_move(opp_move)

            if game_state.checkmate:
                score = -turn * CHECKMATE
            elif game_state.stalemate:
                score = STALEMATE
            else:
                score = -turn * score_material(game_state.board)

            if score > opp_max_score:
                opp_max_score = score

            game_state.undo_move()

        if opp_max_score < opp_minmax_score:
            opp_minmax_score = opp_max_score
            best_player_move = player_move

        game_state.undo_move()

    return best_player_move
