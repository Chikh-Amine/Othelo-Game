import pygame
from othelo.constants import WIDTH, HEIGHT, BLACK, WHITE, GREEN
from othelo.board import Board

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello")

FPS = 60
FONT = pygame.font.SysFont("arial", 28)


def draw_ui(win, board, turn):
    board.draw(win)

    text_color = WHITE if turn == WHITE else BLACK
    turn_text = FONT.render(
        f"Turn: {'WHITE' if turn == WHITE else 'BLACK'}", True, text_color
    )
    score_text = FONT.render(
        f"White: {board.count_white}   Black: {board.count_black}", True, text_color
    )

    win.blit(turn_text, (20, 10))
    win.blit(score_text, (20, 40))


def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()
    turn = BLACK

    while run:
        clock.tick(FPS)

        valid_moves = board.valid_moves(turn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = y // (HEIGHT // 8), x // (WIDTH // 8)

                if board.place_piece(row, col, turn):
                    turn = WHITE if turn == BLACK else BLACK
                else:
                    print("Invalid move")

        if not board.valid_moves(turn):
            other_color = WHITE if turn == BLACK else BLACK
            if not board.valid_moves(other_color):
                winner = board.get_winner()
                print(f"Game Over! Winner: {winner}")
                run = False
            else:
                turn = other_color

        WIN.fill(GREEN)
        draw_ui(WIN, board, turn)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
