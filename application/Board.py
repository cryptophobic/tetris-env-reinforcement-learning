from application.Piece import Piece
import numpy as np


class Board:
    def __init__(self, cols: int, rows: int):
        self.cols: int = cols
        self.rows: int = rows
        self.board = np.zeros((rows, cols), dtype=np.int8)

    def reset_board(self):
        self.board.fill(0)

    def is_collision(self, piece: Piece) -> bool:
        """Check if the current piece collides with the board or boundaries"""
        shape = piece.shape
        x, y = piece.x, piece.y
        for i in range(shape.shape[0]):
            for j in range(shape.shape[1]):
                if shape[i, j] and (y + i >= self.rows or x + j < 0 or x + j >= self.cols or self.board[y + i, x + j]):
                    return True
        return False

    def merge_piece(self, piece: Piece):
        """Merge the current piece into the board"""
        shape = piece.shape
        x, y = piece.x, piece.y
        for i in range(shape.shape[0]):
            for j in range(shape.shape[1]):
                if shape[i, j]:
                    self.board[y + i, x + j] = 1

    def clear_lines(self):
        full_rows = [i for i in range(self.rows) if np.all(self.board[i, :])]
        lines_cleared = len(full_rows)
        for row in full_rows:
            self.board[1:row + 1, :] = self.board[:row, :]
            self.board[0, :] = 0

        return lines_cleared