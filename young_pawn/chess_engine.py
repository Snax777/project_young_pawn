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
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.white_to_move = True
        self.move_log = []
