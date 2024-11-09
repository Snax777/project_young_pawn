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

    load_images()

    running = True

    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

        draw_game_state(screen, game_state)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
