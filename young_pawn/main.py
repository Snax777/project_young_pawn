"""
The main file -- it's responsible for the user input and displaying the current 
GameState object.
"""

import pygame as p
import chess_engine


WIDTH = HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


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


def draw_board(screen):
    """
    Draws squares on the board.
    """

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


def draw_game_state(screen, game_state):
    """
    Responsible for all graphics in current game state.
    """

    draw_board(screen)
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

    load_images()

    running = True
    square_selected = ()
    player_clicks = []

    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
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
                        game_state.board[player_clicks[0][0]][player_clicks[0][-1]][-1]
                        != "p"
                    ):
                        chess_piece = game_state.board[player_clicks[0][0]][
                            player_clicks[0][-1]
                        ][-1]
                    else:
                        chess_piece = ""

                    print(f"{chess_piece}{move.get_chess_notation()}")

                    if move in valid_moves:
                        game_state.make_move(move)
                        move_made = True
                        square_selected = ()
                        player_clicks = []
                    else:
                        player_clicks = [square_selected]
            elif event.type == p.KEYDOWN:
                if event.key == p.K_z:
                    game_state.undo_move()
                    move_made = True

        if move_made:
            valid_moves = game_state.get_valid_moves()
            move_made = False

        draw_game_state(screen, game_state)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
