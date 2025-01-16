"""
This AI will select chess moves that it sees fit for the current position.
"""

import random as r
from copy import deepcopy


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
white_pawn_scores = [
    [0 * val for val in range(8)],
    [0.5, 0.75, 1.0, 1.5, 1.5, 1.0, 0.75, 0.5],
    [0.5, 0.8, 1.25, 1.75, 1.75, 1.25, 0.8, 5],
    [0.5, 1.0, 1.5, 2.0, 2.0, 1.5, 1.0, 0.5],
    [1.0, 1.5, 2.0, 2.5, 2.5, 2.0, 1.5, 1.0],
    [1.5, 2.0, 2.75, 3.5, 3.5, 2.75, 2.0, 1.5],
    [2.5, 3.0, 4.25, 5.5, 5.5, 4.25, 3.0, 2.5],
    [0 * val for val in range(8)],
]
black_pawn_scores = [white_pawn_scores[row] for row in range(7, -1, -1)]
knight_scores = [
    [1 for num in range(8)],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1 for num in range(8)],
]
bishop_scores = deepcopy(knight_scores)
rook_scores = [
    [4 for num in range(8)],
    [3 for num in range(8)],
    [2 for num in range(8)],
    [1 for num in range(8)],
    [1 for num in range(8)],
    [2 for num in range(8)],
    [3 for num in range(8)],
    [4 for num in range(8)],
]
queen_scores = deepcopy(knight_scores)
white_king_scores = [
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-2, -3, -3, -4, -4, -3, -3, -2],
    [-1, -2, -2, -2, -2, -2, -2, -1],
    [2, 2, 0, 0, 0, 0, 2, 2],
    [2, 3, 1, 0, 0, 1, 3, 2],
]
black_king_scores = [white_king_scores[row] for row in range(7, -1, -1)]
piece_position_score = {
    "wp": white_pawn_scores,
    "bp": black_pawn_scores,
    "N": knight_scores,
    "B": bishop_scores,
    "R": rook_scores,
    "Q": queen_scores,
    "wK": white_king_scores,
    "bK": black_king_scores,
}


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


def weighted_score_board(game_state):
    if game_state.checkmate:
        if game_state.white_to_move:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif game_state.stalemate:
        return STALEMATE

    score = 0

    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):
            square = game_state.board[row][col]

            if square != "--":
                pos_score = 0

                if square[1] == "p":
                    pos_score = piece_position_score[square][row][col]
                elif square[1] == "N":
                    pos_score = piece_position_score[square[1]][row][col]
                elif square[1] == "B":
                    pos_score = piece_position_score[square[1]][row][col]
                elif square[1] == "R":
                    pos_score = piece_position_score[square[1]][row][col]
                elif square[1] == "Q":
                    pos_score = piece_position_score[square[1]][row][col]
                elif square[1] == "K":
                    pos_score = piece_position_score[square][row][col]

                if square[0] == "w":
                    score += piece_value[square[1]] + pos_score * 0.5
                elif square[0] == "b":
                    score -= piece_value[square[1]] + pos_score * 0.5

    return score


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


def find_move_nega_max(game_state, valid_moves, depth, turn):
    """
    Uses the NegaMax algorithm to find the best move at n depths.
    """

    global next_move

    if depth == 0:
        return turn * score_board(game_state)

    max_score = -CHECKMATE

    for move in valid_moves:
        game_state.make_move(move)

        next_moves = game_state.get_valid_moves()
        score = -find_move_nega_max(game_state, next_moves, depth - 1, -turn)

        if score > max_score:
            max_score = score

            if depth == DEPTH:
                next_move = move

        game_state.undo_move()

    return max_score


def find_best_move_nega_max(game_state, valid_moves):
    """
    Finds the best move from the NegaMax algorithm.
    """

    global next_move

    next_move = None
    turn_mul = 1 if game_state.white_to_move else -1

    r.shuffle(valid_moves)
    find_move_nega_max(game_state, valid_moves, DEPTH, turn_mul)

    return next_move


def find_best_move_nega_max_alpha_beta(game_state, valid_moves):
    global next_move

    next_move = None
    turn_mul = 1 if game_state.white_to_move else -1

    r.shuffle(valid_moves)

    temp_castling_rights = game_state.castling_rights.copy()

    find_move_nega_max_alpha_beta(
        game_state,
        valid_moves,
        DEPTH,
        -CHECKMATE,
        CHECKMATE,
        turn_mul,
        temp_castling_rights,
    )

    return next_move


def find_move_nega_max_alpha_beta(
    game_state, valid_moves, depth, alpha, beta, turn, temp_castling_rights
):
    global next_move

    if depth == 0:
        return turn * weighted_score_board(game_state)

    max_score = -CHECKMATE

    for move in valid_moves:
        game_state.make_move(move)

        saved_castling_rights = game_state.castling_rights.copy()

        game_state.update_castling_rights(move)

        next_moves = game_state.get_valid_moves()
        score = -find_move_nega_max_alpha_beta(
            game_state,
            next_moves,
            depth - 1,
            -beta,
            -alpha,
            -turn,
            temp_castling_rights,
        )

        if score > max_score:
            max_score = score

            if depth == DEPTH:
                next_move = move

        game_state.undo_move()

        game_state.castling_rights = saved_castling_rights

        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break

    return max_score
