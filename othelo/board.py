import pygame
from .constants import GREEN, ROWS, SQUARE_SIZE, COLS, PADDING, BLACK, WHITE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.count_white = 2
        self.cout_black = 2
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
                if (row == ROWS // 2 - 1 and col == COLS // 2 - 1) or (row == ROWS // 2 and col == COLS // 2):
                    self.board[row].append(Piece(row, col, WHITE))
                elif (row == ROWS // 2 - 1 and col == COLS // 2) or (row == ROWS // 2 and col == COLS // 2 - 1):
                    self.board[row].append(Piece(row, col, BLACK))
                else:
                    self.board[row].append(0)

    
        print("Board structure:", len(self.board), [len(r) for r in self.board])

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
