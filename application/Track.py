from typing import List, Tuple

import numpy as np

from application.Board import Board
from application.Perform import Action
from application.Piece import Piece


class Track:
    def __init__(self, board: Board, initial_reward: float = 0, initial_penalty: float = 0):
        self.board = board
        self.reward = initial_reward
        self.penalty = initial_penalty
        self.action_count: int = 0
        self.drop_count: int = 0
        self.actions_per_drop: List = []
        self.lines_cleared: int = 0
        self.actions: List = []

    def action(self, action: Action):
        self.action_count += 1
        self.actions_per_drop.append(action)

    def drop(self):
        self.actions.extend(self.actions_per_drop)
        self.actions.append(-1)
        self.actions_per_drop.clear()
        self.drop_count += 1

    def calculate_max_height(self):
        """Calculate the maximum height of stacked pieces."""
        for row in range(self.board.rows):
            if np.any(self.board[row, :]):  # If any block exists in the row
                return self.board.rows - row  # Height from the bottom
        return 0  # If board is empty

    def count_holes_and_height(self) -> Tuple[int, int]:
        """Count the number of holes in the board (empty spaces beneath filled blocks)."""
        holes = 0
        height = 0
        for col in range(self.board.cols):
            filled = False  # Tracks if we have encountered a filled cell
            for row in range(self.board.rows):
                if self.board.board[row, col] == 1:
                    filled = True  # Found a filled block
                    current_height = self.board.rows - row
                    if current_height > height:
                        height = current_height
                elif self.board.board[row, col] == 0 and filled:
                    holes += 1  # Empty space below a filled block is a hole
        return holes, height

    def calculate_drop_efficiency(self, piece: Piece):
        """Calculate how well a piece is placed based on neighboring blocks."""
        shape = piece.shape
        x, y = piece['x'], piece['y']
        score = 0

        for i in range(len(shape)):
            check_piece_next = True if x == 0 else False
            check_board_next = False

            if check_piece_next is False and self.board[y + i, x - 1] == 1:
                check_piece_next = True

            for j in range(len(shape[i])):
                if check_piece_next is True:
                    check_piece_next = False
                    if shape[i, j] == 1:
                        score += 1

                if check_board_next is True:
                    check_board_next = False
                    if self.board[y + i, x + j] == 1:
                        score += 1

                if shape[i, j] == 1:
                    check_board_next = True
                elif self.board[y + i, x + j] == 1:
                    check_piece_next = True

            if check_board_next is True:
                j = len(shape[i])
                if j + x >= self.cols or self.board[y + i, x + j] == 1:
                    score += 1
        return score


