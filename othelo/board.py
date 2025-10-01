import pygame
from .constants import GREEN, ROWS, SQUARE_SIZE, COLS, PADDING, BLACK
class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.init_white = self.init_black = 2
        self.count_white = 2
        self.cout_black = 2

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(win,GREEN , (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE - PADDING, SQUARE_SIZE - PADDING))  
