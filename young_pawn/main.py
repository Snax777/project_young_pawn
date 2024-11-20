"""
The main file -- it's responsible for the user input and displaying the current 
GameState object.
"""

import pygame as p
import chess_engine, chess_ai


WIDTH = HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def draw_board(screen):
    """
    Draws squares on the board.
    """
    global colors

    colors = [p.Color("white"), p.Color("gray")]

    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]

            p.draw.rect(
                screen,
                color,
                p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            )


def draw_pieces(screen, board):
    """
    Adds pieces to the board.
    """

    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]

            if piece != "--":
                screen.blit(
                    IMAGES[piece],
                    p.Rect(
                        col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
                    ),
                )


def load_images():
    """
    Creates a global dictionary of images. This will be called once in the main function.
    """

    pieces = ["wp", "bp", "wN", "bN", "wB", "bB", "wR", "bR", "wQ", "bQ", "wK", "bK"]

    for piece in pieces:
        """
        Maps chess piece to appropriate key, and transforms the size of chess piece.
        """
        IMAGES[piece] = p.transform.scale(
            p.image.load(f"images/{piece}.png"), (SQUARE_SIZE, SQUARE_SIZE)
        )


def highlight_squares(screen, game_state, valid_moves, square_selected):
    """
    Highlights selected piece & squares a selected piece can move to.
    """
    if square_selected != ():
        row, col = square_selected

        if game_state.board[row][col][0] == ("w" if game_state.white_to_move else "b"):
            square = p.Surface((SQUARE_SIZE, SQUARE_SIZE))

            square.set_alpha(100)
            square.fill(p.Color("red"))
            screen.blit(square, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            square.fill(p.Color("blue"))

            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(
                        square, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE)
                    )


def animate_move(move, screen, board, clock):
    """
    Animates movement of chess piece(s).
    """
    global colors

    row_diff = move.end_row - move.start_row
    col_diff = move.end_col - move.start_col

    frames_per_square = 5
    frame_count = max(abs(row_diff), abs(col_diff)) * frames_per_square

    for frame in range(frame_count + 1):
        row = move.start_row + (row_diff * frame / frame_count)
        col = move.start_col + (col_diff * frame / frame_count)

        draw_board(screen)
        draw_pieces(screen, board)

        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(
            move.end_col * SQUARE_SIZE,
            move.end_row * SQUARE_SIZE,
            SQUARE_SIZE,
            SQUARE_SIZE,
        )
        p.draw.rect(screen, color, end_square)

        if move.piece_captured != "--":
            screen.blit(IMAGES[move.piece_captured], end_square)

        moving_piece_rect = p.Rect(
            col * SQUARE_SIZE,
            row * SQUARE_SIZE,
            SQUARE_SIZE,
            SQUARE_SIZE,
        )
        screen.blit(IMAGES[move.piece_moved], moving_piece_rect)

        p.display.flip()
        clock.tick(60)


def draw_text(screen, text):
    font = p.font.SysFont("Helvitca", 40, True)
    text_object = font.render(text, 0, p.Color("Black"))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(
        (WIDTH / 2) - (text_object.get_width() / 2),
        (HEIGHT / 2) - (text_object.get_height() / 2),
    )

    screen.blit(text_object, text_location)

    text_object = font.render(text, 0, p.Color("Gray"))

    screen.blit(text_object, text_location.move(2, 2))


def draw_game_state(screen, game_state, valid_moves, square_selected):
    """
    Responsible for all graphics in current game state.
    """

    draw_board(screen)
    highlight_squares(screen, game_state, valid_moves, square_selected)
    draw_pieces(screen, game_state.board)


def main():
    """
    The main function -- handles user input and updates graphics.
    """

    p.init()

    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()

    screen.fill(p.Color("white"))

    game_state = chess_engine.GameState()
    valid_moves = game_state.get_valid_moves()
    move_made = False
    animate = False

    load_images()

    running = True
    square_selected = ()
    player_clicks = []
    game_over = False
    player_one = True
    player_two = False

    while running:
        human_to_play = (game_state.white_to_move and player_one) or (
            (not game_state.white_to_move) and player_two
        )

        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                if not game_over and human_to_play:
                    location = p.mouse.get_pos()
                    col = location[0] // SQUARE_SIZE
                    row = location[-1] // SQUARE_SIZE

                    if square_selected == (row, col):
                        square_selected = ()
                        player_clicks = []
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)

                    if len(player_clicks) == 2:
                        move = chess_engine.Move(
                            player_clicks[0], player_clicks[-1], game_state.board
                        )

                        if (
                            game_state.board[player_clicks[0][0]][player_clicks[0][-1]][
                                -1
                            ]
                            != "p"
                        ):
                            chess_piece = game_state.board[player_clicks[0][0]][
                                player_clicks[0][-1]
                            ][-1]
                        else:
                            chess_piece = ""

                        print(f"{chess_piece}{move.get_chess_notation()}")

                        for val in range(len(valid_moves)):
                            if move == valid_moves[val]:
                                game_state.make_move(valid_moves[val])
                                move_made = True
                                animate = True
                                square_selected = ()
                                player_clicks = []

                        if not move_made:
                            player_clicks = [square_selected]
            elif event.type == p.KEYDOWN:
                if event.key == p.K_z:
                    game_state.undo_move()
                    valid_moves = game_state.get_valid_moves()
                    move_made = True
                    animate = False

                if event.key == p.K_r:
                    game_state = chess_engine.GameState()
                    valid_moves = game_state.get_valid_moves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False

        if not game_over and not human_to_play:
            ai_move = chess_ai.find_random_move(valid_moves)

            game_state.make_move(ai_move)

            move_made = True
            animate = True

        if move_made:
            if animate:
                animate_move(game_state.move_log[-1], screen, game_state.board, clock)

            valid_moves = game_state.get_valid_moves()
            move_made = False
            animate = False

        draw_game_state(screen, game_state, valid_moves, square_selected)

        if game_state.checkmate:
            game_over = True

            if game_state.white_to_move:
                draw_text(screen, "Black wins")
            else:
                draw_text(screen, "White wins")
        elif game_state.stalemate:
            game_over = True

            draw_text(screen, "Stalemate")

        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
