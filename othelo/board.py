import pygame
from .constants import COLS, GREEN, ROWS, COLS, SQUARE_SIZE, PADDING, BLACK, WHITE
from .piece import Piece

class Board:
    """Handles the board state and game rules"""

    # all the the checking directions:
    DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def __init__(self):
        self.board = []
        self.white_count = 2
        self.black_count = 2
        self.create_board()

    def create_board(self):
        """initialize the board with starting pieces"""

        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                # starting position
                if (row == 3 and col == 3) or (row == 4 and col == 4):
                    self.board[row].append(Piece(row, col, WHITE))
                elif (row == 3 and col == 4) or (row == 4 and col == 3):
                    self.board[row].append(Piece(row, col, BLACK))
                else:
                    self.board[row].append(0)

    def draw_squares(self, win):
        """Draw the board grid"""
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(
                    win,
                    GREEN,
                    (
                        col * SQUARE_SIZE,
                        row * SQUARE_SIZE,
                        SQUARE_SIZE - PADDING,
                        SQUARE_SIZE - PADDING,
                    ),
                )

    def draw(self, win):
        """draw the entire board with pieces"""
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def get_valid_moves(self, color):
        """
        Returns a dictionary of valid moves for the given color.
        Key: (row, col) tuple
        Value: list of (row, col) tuples of pieces that would be flipped
        """
        opponent = BLACK if color == WHITE else WHITE
        valid_moves = {}

        for row in range(ROWS):
            for col in range(COLS):
                # Skip occupied squares
                if self.board[row][col] != 0:
                    continue

                pieces_to_flip = []

                # Check all 8 directions
                for dr, dc in self.DIRECTIONS:
                    current_flip_list = []
                    r, c = row + dr, col + dc

                    # Collect opponent pieces in this direction
                    while (
                        0 <= r < ROWS
                        and 0 <= c < COLS
                        and self.board[r][c] != 0
                        and self.board[r][c].color == opponent
                    ):
                        current_flip_list.append((r, c))
                        r += dr
                        c += dc

                    # Valid if we hit our own piece after opponent pieces
                    if (
                        current_flip_list
                        and 0 <= r < ROWS
                        and 0 <= c < COLS
                        and self.board[r][c] != 0
                        and self.board[r][c].color == color
                    ):
                        pieces_to_flip.extend(current_flip_list)

                # If we can flip pieces, this is a valid move
                if pieces_to_flip:
                    valid_moves[(row, col)] = pieces_to_flip

        return valid_moves

    def make_move(self, row, col, color):
        """
        Place a piece and flip captured pieces.
        Retruns True if move was valid, Fals otherwise
        """
        valid_moves = self.get_valid_moves(color)

        if (row, col) not in valid_moves[(row, col)]:
            return False

        # place the piece
        self.board[row][col] = Piece(row, col, color)

        # flip all captured pieces
        for r, c in valid_moves[(row, col)]:
            self.board[r][c].color = color

        self.update_counts()
        return True

    def update_counts(self):
        """Update the piece count for both colors"""
        white = 0
        black = 0

        for row in self.board:
            for piece in row:
                if piece != 0:
                    if piece.color == WHITE:
                        white += 1
                    else:
                        black += 1

        self.white_count = white
        self.black_count = black

    def is_game_over(self):
        """check if neither player has bvalid moves"""

        return (
            len(self.get_valid_moves(WHITE)) == 0
            and len(self.get_valid_moves(BLACK)) == 0
        )

    def get_winner(self):
        """return the winner"""
        if self.white_count > self.black_count:
            return "WHITE"
        elif self.black_count > self.white_count:
            return "BLACK"
        else:
            return "DRAW"

    def get_piece(self, row, col):
        """get the piece at the given position"""
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.board[row][col]
        return None
