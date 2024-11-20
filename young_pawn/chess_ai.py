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
DEPTH = 2


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
    Selects move based on current value for White and Black.
    """
    turn = 1 if game_state.white_to_move else -1
    opp_minmax_score = CHECKMATE
    best_player_move = None

    r.shuffle(valid_moves)

    for player_move in valid_moves:
        game_state.make_move(player_move)

        opp_moves = game_state.get_valid_moves()

        if game_state.stalemate:
            opp_max_score = STALEMATE
        elif game_state.checkmate:
            opp_max_score = -CHECKMATE
        else:
            opp_max_score = -CHECKMATE

            for opp_move in opp_moves:
                game_state.make_move(opp_move)
                game_state.get_valid_moves()

                if game_state.checkmate:
                    score = CHECKMATE
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


def find_best_move_min_max(game_state, valid_moves):
    """
    Helper function for `find_recursive_minmax_move`
    """
    global next_move
    next_move = None

    find_recursive_minmax_move(game_state, valid_moves, DEPTH, game_state.white_to_move)

    return next_move


def find_recursive_minmax_move(game_state, valid_moves, depth, white_to_move):
    """
    Finds best move with recursive MinMax algorithm.
    """
    global next_move

    if depth == 0:
        return score_material(game_state.board)

    if white_to_move:
        max_score = -CHECKMATE

        for move in valid_moves:
            game_state.make_move(move)

            next_moves = game_state.get_valid_moves()
            score = find_recursive_minmax_move(game_state, next_moves, depth - 1, False)

            if score > max_score:
                max_score = score

                if depth == DEPTH:
                    next_move = move

            game_state.undo_move()

        return max_score
    else:
        min_score = CHECKMATE

        for move in valid_moves:
            game_state.make_move(move)

            next_moves = game_state.get_valid_moves()
            score = find_recursive_minmax_move(game_state, next_moves, depth - 1, True)

            if score < min_score:

                min_score = score
                if depth == DEPTH:
                    next_move = move

            game_state.undo_move()

        return min_score


def score_board(game_state):
    if game_state.checkmate:
        if game_state.white_to_move:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif game_state.stalemate:
        return STALEMATE

    score = 0

    for row in game_state.board:
        for square in row:
            if square[0] == "w":
                score += piece_value[square[1]]
            elif square[0] == "b":
                score -= piece_value[square[1]]

    return score
