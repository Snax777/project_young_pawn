class GameState:
    """
    This class is responsible for storing all the information about the
    current state of a chess game. It's also responsible for determining valid
    moves at the current state. It will also keep a move log.
    """

    def __init__(self):
        """
        Board is an 8-by-8 2D list, each element of the list has 2 characters
        The first character represents the colour of the piece, 'b' or 'w',
        and the second character represents the type of piece, 'p', 'N', 'B',
        'R', 'Q', and 'K'.
        The string '--' represents an empty square.
        """
        self.pieces = ["R", "N", "B", "Q", "K", "B", "N", "R"]
        self.board = [
            [f"b{piece}" for piece in self.pieces],
            ["bp" for num in range(8)],
            ["--" for num in range(8)],
            ["--" for num in range(8)],
            ["--" for num in range(8)],
            ["--" for num in range(8)],
            ["wp" for num in range(8)],
            [f"w{piece}" for piece in self.pieces],
        ]
        self.white_to_move = True
        self.move_log = []

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        """
        Deletes the last move made.
        """
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

    def get_valid_moves(self):
        """
        Gets valid/legal chess moves when king is in check.
        """
        return self.get_all_possible_moves()

    def get_all_possible_moves(self):
        """
        Gets all possible valid moves.
        """
        possible_moves = []

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                piece_color = self.board[row][col][0]

                if (piece_color == "w" and self.white_to_move) and (
                    piece_color == "b" and not self.white_to_move
                ):
                    piece = self.board[row][col][-1]

                    if piece == "p":
                        self.get_pawn_moves(row, col, possible_moves)
                    elif piece == "N":
                        self.get_knight_moves(row, col, possible_moves)
                    elif piece == "B":
                        self.get_bishop_moves(row, col, possible_moves)
                    elif piece == "R":
                        self.get_rook_moves(row, col, possible_moves)
                    elif piece == "Q":
                        self.get_queen_moves(row, col, possible_moves)
                    else:
                        self.get_king_moves(row, col, possible_moves)

        return possible_moves


class Move:
    RANKS_TO_ROWS = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    ROWS_TO_RANKS = {v: k for k, v in RANKS_TO_ROWS.items()}
    FILES_TO_COLS = {chr(97 + num): num for num in range(8)}
    COLS_TO_FILES = {v: k for k, v in FILES_TO_COLS.items()}

    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_col = start_square[-1]
        self.end_row = end_square[0]
        self.end_col = end_square[-1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = (
            (self.start_row * 1000)
            + (self.start_col * 100)
            + (self.end_row * 10)
            + self.end_col
        )
        print(self.move_id)

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id

        return False

    def get_chess_notation(self):
        start = self.get_rank_file(self.start_row, self.start_col)
        end = self.get_rank_file(self.end_row, self.end_col)

        return f"{start}-{end}"

    def get_rank_file(self, row, col):
        return Move.COLS_TO_FILES[col] + Move.ROWS_TO_RANKS[row]
