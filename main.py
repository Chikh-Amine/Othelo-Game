
# main.py
import sys
import pygame
from othelo.game import Game
from othelo.piece import Piece
from othelo.constants import SQUARE_SIZE, COLS, ROWS, FPS

# window size
WIDTH = COLS * SQUARE_SIZE
HEIGHT = ROWS * SQUARE_SIZE


def apply_move(board, move, color):
    """
    Temporary helper because Board.make_move currently has a small bug.
    Applies a move using Board.get_valid_moves().
    """
    valid = board.get_valid_moves(color)
    if move not in valid:
        return False

    row, col = move
    board.board[row][col] = Piece(row, col, color)
    for r, c in valid[move]:
        board.board[r][c].color = color
    board.update_counts()
    return True


def coords_from_mouse(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return row, col


def draw_scores(win, board, font):
    white = board.white_count
    black = board.black_count
    text = f"BLACK: {black}    WHITE: {white}"
    surf = font.render(text, True, (255, 255, 255))
    win.blit(surf, (10, 10))


def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Othello — Man vs Man")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    game = Game(win)
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not game.is_game_over():
                    pos = pygame.mouse.get_pos()
                    row, col = coords_from_mouse(pos)
                    board = game.get_board()
                    turn = game.get_turn()
                    valid_moves = board.get_valid_moves(turn)
                    if (row, col) in valid_moves:
                        applied = apply_move(board, (row, col), turn)
                        if applied:
                            game._change_turn()

            if event.type == pygame.KEYDOWN:
                # press R to restart
                if event.key == pygame.K_r:
                    game.reset()

        # draw board and UI
        game.update()
        draw_scores(win, game.get_board(), font)

        if game.is_game_over():
            winner = game.get_board().get_winner()
            msg = f"Game Over: {winner}  (Press R to restart)"
            surf = font.render(msg, True, (255, 255, 255))
            win.blit(surf, (10, 30))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
