import pygame
from .constants import GREEN, ROWS, SQUARE_SIZE, COLS, PADDING, BLACK, WHITE
from .piece import Piece


class Board:

    DIRECTIONS = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]

    def __init__(self):
        self.board = []
        self.count_white = 2
        self.count_black = 2
        self.create_board()

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(
                    win,
                    GREEN,
                    (
                        row * SQUARE_SIZE,
                        col * SQUARE_SIZE,
                        SQUARE_SIZE - PADDING,
                        SQUARE_SIZE - PADDING,
                    ),
                )

    def create_board(self):
        self.board = []

        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if (row == ROWS // 2 - 1 and col == COLS // 2 - 1) or (
                    row == ROWS // 2 and col == COLS // 2
                ):
                    self.board[row].append(Piece(row, col, WHITE))
                elif (row == ROWS // 2 - 1 and col == COLS // 2) or (
                    row == ROWS // 2 and col == COLS // 2 - 1
                ):
                    self.board[row].append(Piece(row, col, BLACK))
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def valid_moves(self, color):
        opponent = BLACK if color == WHITE else WHITE
        moves = {}

        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] != 0:
                    continue
                pieces_to_flip = []
                for dr, dc in self.DIRECTIONS:
                    r, c = row + dr, col + dc
                    pieces = []
                    while (
                        0 <= r < ROWS
                        and 0 <= c < COLS
                        and self.board[r][c] != 0
                        and self.board[r][c].color == opponent
                    ):
                        pieces.append((r, c))
                        r += dr
                        c += dc
                    if (
                        0 <= r < ROWS
                        and 0 <= c < COLS
                        and self.board[r][c] != 0
                        and self.board[r][c].color == color
                        and pieces
                    ):
                        pieces_to_flip.extend(pieces)
                if pieces_to_flip:
                    moves[(row, col)] = pieces_to_flip

        return moves

    def place_piece(self, row, col, color):
        moves = self.valid_moves(color)
        if (row, col) not in moves:
            return False  # Invalid move

        self.board[row][col] = Piece(row, col, color)

        # Flip captured pieces
        for r, c in moves[(row, col)]:
            self.board[r][c].color = color

        self.update_counts()
        return True

    def update_counts(self):
        white, black = 0, 0
        for row in self.board:
            for piece in row:
                if piece != 0:
                    if piece.color == WHITE:
                        white += 1
                    else:
                        black += 1
        self.count_white = white
        self.count_black = black

    def get_winner(self):
        if self.count_white > self.count_black:
            return "WHITE"
        elif self.count_black > self.count_white:
            return "BLACK"
        else:
            return "DRAW"
