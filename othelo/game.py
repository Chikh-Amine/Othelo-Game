import pygame
from .board import Board
from .constants import WHITE, BLACK, SQUARE_SIZE, GREY


class Game:
    """Main game controllerm, manages turns, state, and flow"""

    def __init__(self, win):
        self.win = win
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}
        self.selected = None
        self.game_over = False
        self.winner = None
        self.pass_count = 0
        self._update_valid_moves()

    def _update_valid_moves(self):
        """calculates valid moves for current player"""
        self.valid_moves = self.board.get_valid_moves(self.turn)

    def update(self):
        """update and draw the game"""
        self.board.draw(self.win)
        self._draw_valid_moves()
        pygame.display.update()

    def _draw_valid_moves(self):
        """draw indicators for valid moves"""
        for row, col in self.valid_moves.keys():
            x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            y = row * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.circle(self.win, GREY, (x, y), 8)

    def select(self, row, col):
        """
        attempt to place a piece at (row, col).
        returns true if move was successfil.
        """
        if self.game_over:
            return False

        if (row, col) in self.valid_moves:
            self.board.make_move(row, col, self.turn)
            self.pass_count = 0
            self._change_turn()
            return True

        return False

    def _change_turn(self):
        """switch turn to other player"""
        self.turn = WHITE if self.turn == BLACK else BLACK
        self._update_valid_moves()

        if not self.valid_moves:
            self.pass_count += 1

            self.turn = WHITE if self.turn == BLACK else WHITE
            self._update_valid_moves()

            if not self.valid_moves or self.pass_count >= 2:
                self.game_over = True
                self.winner = self.board.get_winner()
        else:
            self.pass_count = 0

    def reset(self):
        """reset the game to its initial state"""
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}
        self.selected = None
        self.game_over = False
        self.winner = None
        self.pass_count = 0
        self._update_valid_moves()

    def get_board(self):
        """get the board object"""
        return self.board

    def get_turn(self):
        """get the current players color"""
        return self.turn

    def is_game_over(self):
        """check of game is over"""
        return self.game_over
