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
        self.move_functions = {
            "p": self.get_pawn_moves,
            "N": self.get_knight_moves,
            "B": self.get_bishop_moves,
            "R": self.get_rook_moves,
            "Q": self.get_queen_moves,
            "K": self.get_king_moves,
        }
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.en_passant_possible = ()
        self.castling_rights = Castling(True, True, True, True)
        self.castling_log = [
            Castling(
                self.castling_rights.w_kingside,
                self.castling_rights.w_queenside,
                self.castling_rights.b_kingside,
                self.castling_rights.b_queenside,
            )
        ]

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)

        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + "Q"

        if move.is_en_passant:
            self.board[move.start_row][move.end_col] = "--"

        if move.piece_moved[-1] == "p" and abs(move.start_row - move.end_row) == 2:
            self.en_passant_possible = (
                (move.start_row + move.end_row) // 2,
                move.start_col,
            )
        else:
            self.en_passant_possible = ()

        if move.castling:
            if move.end_col - move.start_col == 2:
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][
                    move.end_col + 1
                ]
                self.board[move.end_row][move.end_col + 1] = "--"
            else:
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][
                    move.end_col - 2
                ]
                self.board[move.end_row][move.end_col - 2] = "--"

        self.update_castling_rights(move)
        self.castling_log.append(
            Castling(
                self.castling_rights.w_kingside,
                self.castling_rights.w_queenside,
                self.castling_rights.b_kingside,
                self.castling_rights.b_queenside,
            )
        )

    def undo_move(self):
        """
        Deletes the last move made.
        """
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

            if move.piece_moved == "wK":
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_col)

            if move.is_en_passant:
                self.board[move.end_row][move.end_col] = "--"
                self.board[move.start_row][move.end_col] = move.piece_captured
                self.en_passant_possible = (move.end_row, move.end_col)

            if move.piece_moved[-1] == "p" and abs(move.start_row - move.end_row) == 2:
                self.en_passant_possible = ()

            self.castling_log.pop()

            self.castling_rights = self.castling_log[-1]

            if move.castling:
                if move.piece_moved == "wK":
                    if move.end_col - move.start_col == 2:
                        self.board[move.end_row][move.end_col + 1] = self.board[
                            move.end_row
                        ][move.end_col - 1]
                        self.board[move.end_row][move.end_col - 1] = "--"
                        self.castling_rights.w_kingside = (
                            True  # Restores right to castle kingside
                        )
                    else:
                        self.board[move.end_row][move.end_col - 2] = self.board[
                            move.end_row
                        ][move.end_col + 1]
                        self.board[move.end_row][move.end_col + 1] = "--"
                        self.castling_rights.w_queenside = (
                            True  # Restores right to castle queenside
                        )
                elif move.piece_moved == "bK":
                    if move.end_col - move.start_col == 2:
                        self.board[move.end_row][move.end_col + 1] = self.board[
                            move.end_row
                        ][move.end_col - 1]
                        self.board[move.end_row][move.end_col - 1] = "--"
                        self.castling_rights.b_kingside = (
                            True  # Restores right to castle kingside
                        )
                    else:
                        self.board[move.end_row][move.end_col - 2] = self.board[
                            move.end_row
                        ][move.end_col + 1]
                        self.board[move.end_row][move.end_col + 1] = "--"
                        self.castling_rights.b_queenside = (
                            True  # Restores right to castle queenside
                        )

    def update_castling_rights(self, move):
        """
        Updates the castling rights if castling has been achieved or any of the rights are violated.
        """
        if move.piece_moved == "wK":
            self.castling_rights.w_kingside = False
            self.castling_rights.w_queenside = False
        elif move.piece_moved == "bK":
            self.castling_rights.b_kingside = False
            self.castling_rights.b_queenside = False
        elif move.piece_moved == "wR":
            if move.start_row == 7:
                if move.start_col == 0:
                    self.castling_rights.w_queenside = False
                elif move.start_col == 7:
                    self.castling_rights.w_kingside = False
        elif move.piece_moved == "bR":
            if move.start_row == 0:
                if move.start_col == 0:
                    self.castling_rights.b_queenside = False
                elif move.start_col == 7:
                    self.castling_rights.b_kingside = False

    def get_valid_moves(self):
        """
        Gets valid/legal chess moves when king is in check.
        """
        temp_en_passant = self.en_passant_possible
        temp_castling_rights = Castling(
            self.castling_rights.w_kingside,
            self.castling_rights.w_queenside,
            self.castling_rights.b_kingside,
            self.castling_rights.b_queenside,
        )
        valid_moves = self.get_all_possible_moves()
        length = len(valid_moves)

        if self.white_to_move:
            self.get_castling_moves(
                self.white_king_location[0], self.white_king_location[-1], valid_moves
            )
        else:
            self.get_castling_moves(
                self.black_king_location[0], self.black_king_location[-1], valid_moves
            )

        for val in range(length - 1, -1, -1):
            self.make_move(valid_moves[val])

            self.white_to_move = not self.white_to_move

            if self.in_check():
                valid_moves.remove(valid_moves[val])

            self.white_to_move = not self.white_to_move

            self.undo_move()

        if len(valid_moves) == 0:
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        self.en_passant_possible = temp_en_passant
        self.castling_rights = temp_castling_rights

        return valid_moves

    def in_check(self):
        """
        Checks if the king -- white or black -- is under attack.
        """
        if self.white_to_move:
            return self.square_under_attack(
                self.white_king_location[0], self.white_king_location[1]
            )
        else:
            return self.square_under_attack(
                self.black_king_location[0], self.black_king_location[1]
            )

    def square_under_attack(self, row, col):
        """
        Looks for squares that are a chess piece's influence.
        """
        self.white_to_move = not self.white_to_move
        opp_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move

        for move in opp_moves:
            if move.end_row == row and move.end_col == col:
                return True

        return False

    def get_all_possible_moves(self):
        """
        Gets all possible valid moves.
        """
        possible_moves = []

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                piece_color = self.board[row][col][0]

                if (piece_color == "w" and self.white_to_move) or (
                    piece_color == "b" and not self.white_to_move
                ):
                    piece = self.board[row][col][-1]

                    self.move_functions[piece](row, col, possible_moves)

        return possible_moves

    def get_pawn_moves(self, row, col, moves) -> list[object]:
        """
        Gets all the valid pawn moves.
        """
        if self.white_to_move:
            if self.board[row - 1][col] == "--":
                moves.append(Move((row, col), (row - 1, col), self.board))

                if self.board[row - 2][col] == "--" and row == 6:
                    moves.append(Move((row, col), (row - 2, col), self.board))
            if col - 1 >= 0:
                if self.board[row - 1][col - 1][0] == "b":
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))

                if (row - 1, col - 1) == self.en_passant_possible:
                    moves.append(
                        Move(
                            (row, col), (row - 1, col - 1), self.board, en_passant=True
                        )
                    )

            if col + 1 <= 7:
                if self.board[row - 1][col + 1][0] == "b":
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))

                if (row - 1, col + 1) == self.en_passant_possible:
                    moves.append(
                        Move(
                            (row, col), (row - 1, col + 1), self.board, en_passant=True
                        )
                    )
        else:
            if self.board[row + 1][col] == "--":
                moves.append(Move((row, col), (row + 1, col), self.board))

                if self.board[row + 2][col] == "--" and row == 1:
                    moves.append(Move((row, col), (row + 2, col), self.board))
            if col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == "w":
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))

                if (row + 1, col - 1) == self.en_passant_possible:
                    moves.append(
                        Move(
                            (row, col), (row + 1, col - 1), self.board, en_passant=True
                        )
                    )

            if col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == "w":
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))

                if (row + 1, col + 1) == self.en_passant_possible:
                    moves.append(
                        Move(
                            (row, col), (row + 1, col + 1), self.board, en_passant=True
                        )
                    )

        return moves

    def get_knight_moves(self, row, col, moves) -> list[object]:
        """
        Gets all the valid knight moves.
        """
        knight_coordinates = [
            (-2, -1),
            (-2, 1),
            (2, -1),
            (2, 1),
            (1, -2),
            (1, 2),
            (-1, -2),
            (-1, 2),
        ]

        if self.white_to_move:
            for coordinates in knight_coordinates:
                coord_row = coordinates[0]
                coord_col = coordinates[-1]

                if (0 <= row + coord_row <= 7) and (0 <= col + coord_col <= 7):
                    if self.board[row + coord_row][col + coord_col][0] in ["b", "-"]:
                        moves.append(
                            Move(
                                (row, col),
                                (row + coord_row, col + coord_col),
                                self.board,
                            )
                        )
        else:
            for coordinates in knight_coordinates:
                coord_row = coordinates[0]
                coord_col = coordinates[-1]

                if (
                    (0 <= row + coord_row <= 7)
                    and (0 <= col + coord_col <= 7)
                    and self.board[row + coord_row][col + coord_col][0] in ["w", "-"]
                ):
                    moves.append(
                        Move((row, col), (row + coord_row, col + coord_col), self.board)
                    )

        return moves

    def get_bishop_moves(self, row, col, moves) -> list[object]:
        """
        Gets all the valid bishop moves.
        """
        bishop_offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        if self.white_to_move:
            for offset in bishop_offsets:
                for num in range(1, 8):
                    off_row = offset[0] * num
                    off_col = offset[1] * num

                    if (0 <= row + off_row <= 7) and (0 <= col + off_col <= 7):
                        if self.board[row + off_row][col + off_col][0] == "b":
                            moves.append(
                                Move(
                                    (row, col),
                                    (row + off_row, col + off_col),
                                    self.board,
                                )
                            )
                            break
                        elif self.board[row + off_row][col + off_col][0] == "-":
                            moves.append(
                                Move(
                                    (row, col),
                                    (row + off_row, col + off_col),
                                    self.board,
                                )
                            )
                        elif self.board[row + off_row][col + off_col][0] == "w":
                            break
        else:
            for offset in bishop_offsets:
                for num in range(1, 8):
                    off_row = offset[0] * num
                    off_col = offset[1] * num

                    if (0 <= row + off_row <= 7) and (0 <= col + off_col <= 7):
                        if self.board[row + off_row][col + off_col][0] == "w":
                            moves.append(
                                Move(
                                    (row, col),
                                    (row + off_row, col + off_col),
                                    self.board,
                                )
                            )
                            break
                        elif self.board[row + off_row][col + off_col][0] == "-":
                            moves.append(
                                Move(
                                    (row, col),
                                    (row + off_row, col + off_col),
                                    self.board,
                                )
                            )
                        elif self.board[row + off_row][col + off_col][0] == "b":
                            break

        return moves

    def get_rook_moves(self, row, col, moves) -> list[object]:
        """
        Gets all the valid rook moves.
        """
        rook_offsets = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        if self.white_to_move:
            for offset in rook_offsets:
                for num in range(1, 8):
                    off_row = offset[0] * num
                    off_col = offset[1] * num

                    if (0 <= row + off_row <= 7) and (0 <= col + off_col <= 7):
                        if self.board[row + off_row][col + off_col][0] == "b":
                            moves.append(
                                Move(
                                    (row, col),
                                    (row + off_row, col + off_col),
                                    self.board,
                                )
                            )
                            break
                        elif self.board[row + off_row][col + off_col][0] == "-":
                            moves.append(
                                Move(
                                    (row, col),
                                    (row + off_row, col + off_col),
                                    self.board,
                                )
                            )
                        else:
                            break
        else:
            for offset in rook_offsets:
                for num in range(1, 8):
                    off_row = offset[0] * num
                    off_col = offset[1] * num

                    if (0 <= row + off_row <= 7) and (0 <= col + off_col <= 7):
                        if self.board[row + off_row][col + off_col][0] == "w":
                            moves.append(
                                Move(
                                    (row, col),
                                    (row + off_row, col + off_col),
                                    self.board,
                                )
                            )
                            break
                        elif self.board[row + off_row][col + off_col][0] == "-":
                            moves.append(
                                Move(
                                    (row, col),
                                    (row + off_row, col + off_col),
                                    self.board,
                                )
                            )
                        else:
                            break

        return moves

    def get_queen_moves(self, row, col, moves) -> list[object]:
        """
        Gets all the valid queen moves.
        """
        self.get_bishop_moves(row, col, moves)
        self.get_rook_moves(row, col, moves)

    def get_king_moves(self, row, col, moves) -> list[object]:
        """
        Gets all the valid king moves.
        """
        king_offsets = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        ally_color = "w" if self.white_to_move else "b"

        if self.white_to_move:
            for offset in king_offsets:
                off_row = offset[0]
                off_col = offset[1]

                if (0 <= row + off_row <= 7) and (0 <= col + off_col <= 7):
                    if self.board[row + off_row][col + off_col][0] != ally_color:
                        moves.append(
                            Move(
                                (row, col),
                                (row + off_row, col + off_col),
                                self.board,
                            )
                        )
        else:
            for offset in king_offsets:
                off_row = offset[0]
                off_col = offset[1]

                if (0 <= row + off_row <= 7) and (0 <= col + off_col <= 7):
                    if self.board[row + off_row][col + off_col][0] != ally_color:
                        moves.append(
                            Move(
                                (row, col),
                                (row + off_row, col + off_col),
                                self.board,
                            )
                        )

    def get_castling_moves(self, row, col, moves):
        """
        Get all valid castling moves for bothe white and black.
        """
        if self.square_under_attack(row, col):
            pass

        if (self.white_to_move and self.castling_rights.w_kingside) or (
            (not self.white_to_move) and self.castling_rights.b_kingside
        ):
            self.get_kingside_castling(row, col, moves)

        if (self.white_to_move and self.castling_rights.w_queenside) or (
            (not self.white_to_move) and self.castling_rights.b_queenside
        ):
            self.get_queenside_castling(row, col, moves)

    def get_kingside_castling(self, row, col, moves):
        if (self.board[row][col + 1] == "--") and (self.board[row][col + 2] == "--"):
            if (not self.square_under_attack(row, col + 1)) and (
                not self.square_under_attack(row, col + 2)
            ):
                moves.append(
                    Move((row, col), (row, col + 2), self.board, castling=True)
                )

    def get_queenside_castling(self, row, col, moves):
        if (
            (self.board[row][col - 1] == "--")
            and (self.board[row][col - 2] == "--")
            and (self.board[row][col - 3])
        ):
            if (not self.square_under_attack(row, col - 1)) and (
                not self.square_under_attack(row, col - 2)
            ):
                moves.append(
                    Move((row, col), (row, col - 2), self.board, castling=True)
                )


class Castling:
    """
    This class implements the castling rights for both black and white on the kingside and queenside.
    """

    def __init__(self, w_kingside, w_queenside, b_kingside, b_queenside):
        self.w_kingside = w_kingside
        self.w_queenside = w_queenside
        self.b_kingside = b_kingside
        self.b_queenside = b_queenside


class Move:
    RANKS_TO_ROWS = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    ROWS_TO_RANKS = {v: k for k, v in RANKS_TO_ROWS.items()}
    FILES_TO_COLS = {chr(97 + num): num for num in range(8)}
    COLS_TO_FILES = {v: k for k, v in FILES_TO_COLS.items()}

    def __init__(
        self, start_square, end_square, board, en_passant=False, castling=False
    ):
        self.start_row = start_square[0]
        self.start_col = start_square[-1]
        self.end_row = end_square[0]
        self.end_col = end_square[-1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.is_pawn_promotion = (self.piece_moved == "wp" and self.end_row == 0) or (
            self.piece_moved == "bp" and self.end_row == 7
        )
        self.is_en_passant = en_passant
        self.castling = castling

        if self.is_en_passant:
            self.piece_captured = "wp" if self.piece_moved == "bp" else "bp"

        self.move_id = (
            (self.start_row * 1000)
            + (self.start_col * 100)
            + (self.end_row * 10)
            + self.end_col
        )

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
