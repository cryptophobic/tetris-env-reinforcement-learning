import os
from typing import List, Tuple, Callable

import numpy as np
import pandas as pd

from application.Board import Board
from application.Perform import Action
from application.Piece import Piece

import inspect


class Track:

    PIECE = 0
    HEIGHT = 1
    HOLES = 2
    DROP_SCORE = 3
    ACTIONS = 4
    LINES_CLEARED = 5
    FLOOR = 6
    COLLISIONS = 7
    GAME_OVER = 8
    RESET = 9

    FLOOR_REWARD = 10
    DROP_REWARD = 11
    LINES_REWARD = 12
    HEIGHT_PENALTY = 13
    DROP_PENALTY = 14
    HOLES_PENALTY = 15

    REWARD = 16
    PENALTY = 17
    REWARD_DIFF = 18
    PENALTY_DIFF = 19

    HEADER = ['PIECE', "HEIGHT", "HOLES", "DROP_SCORE", "ACTIONS", "LINES_CLEARED",
            "FLOOR", "COLLISIONS", "GAME_OVER", "RESET", "FLOOR_REWARD",
            "DROP_REWARD", "LINES_REWARD", "HEIGHT_PENALTY", "DROP_PENALTY",
            "HOLES_PENALTY", "REWARD", "PENALTY", "REWARD_DIFF", "PENALTY_DIFF"]

    def __init__(self,
                 board: Board,
                 buffer_size=4096,
                 save_path="tetris_stats.csv"
                 ):
        self.board = board
        self.reward: float = 0
        self.penalty: float = 0
        self.buffer_size = buffer_size
        self.save_path = save_path
        self.index = 0  # Track current buffer position

        self.data_buffer = np.zeros(shape=(buffer_size, 20), dtype=float)

        self.heights: List[int] = []
        self.holes: List[int] = []
        self.actions_per_drop: int = 0
        self.collisions_per_drop = 0
        self.actions_per_drop_count: List[int] = []
        self.lines_cleared: List[int] = []
        self.actions: List[int] = []

    def action_wrapper(self, method: Callable):
        def wrapper(*args, **kwargs):
            # TODO: example of args extracting
            # sig = inspect.signature(method)
            # bound_args = sig.bind(*args, **kwargs)
            # bound_args.apply_defaults()  # Apply default values if missing

            # action = bound_args.arguments.get('action')
            # self.actions_per_drop.append(action)
            self.actions_per_drop += 1
            result = method(*args, **kwargs)

            return result

        return wrapper

    def fail_wrapper(self, method: Callable):
        def wrapper(*args, **kwargs):
            result = method(*args, **kwargs)
            self.collisions_per_drop += 1

            return result

        return wrapper

    def drop_wrapper(self, method: Callable):
        def wrapper(*args, **kwargs):
            piece = method(*args, **kwargs)
            self.data_buffer[self.index][self.ACTIONS] = self.actions_per_drop
            self.data_buffer[self.index][self.DROP_SCORE] = self.calculate_drop_efficiency(piece)
            self.data_buffer[self.index][self.COLLISIONS] = self.collisions_per_drop
            # self.actions_per_drop_count.append(len(self.actions_per_drop))
            self.actions_per_drop = 0
            self.collisions_per_drop = 0

            return piece

        return wrapper

    def merge_wrapper(self, method):
        def wrapper(*args, **kwargs):
            result = method(*args, **kwargs)
            holes, height = self.count_holes_and_height()
            self.data_buffer[self.index][self.HOLES] = holes
            self.data_buffer[self.index][self.HEIGHT] = height

            return result

        return wrapper

    def clear_lines_wrapper(self, method):
        def wrapper(*args, **kwargs):
            lines_number = method(*args, **kwargs)
            """Could be zero"""
            self.data_buffer[self.index][self.LINES_CLEARED] = lines_number

            return lines_number

        return wrapper

    def set_game_over_wrapper(self, method):
        def wrapped(*args, **kwargs):
            result = method(*args, **kwargs)
            self.data_buffer[self.index][self.GAME_OVER] = 1
            self.reward = 0
            self.penalty = 0
            return result

        return wrapped

    def reset_wrapper(self, method):
        def wrapped(*args, **kwargs):
            result = method(*args, **kwargs)
            self.data_buffer[self.index][self.RESET] = 1
            self.reward = 0
            self.penalty = 0
            return result

        return wrapped

    def spawn_piece_wrapper(self, method):
        """Decorator to wrap Engine.spawn_piece"""
        def wrapped(*args, **kwargs):
            result = method(*args, **kwargs)  # Call the original spawn_piece
            if self.index >= self.buffer_size:
                self.flush_to_disk()
            return result  # Preserve return value if needed

        return wrapped

    # 1 line = 1
    # 2 lines = 3
    # 3 lines = 5
    # 4 lines = 10
    def calculate_reward_penalty(self):
        efficient_drop = self.data_buffer[self.index][self.DROP_SCORE]
        current_height = self.data_buffer[self.index][self.HEIGHT]
        last_height = 0 if self.index == 0 else self.data_buffer[self.index - 1][self.HEIGHT]
        lines_cleared = self.data_buffer[self.index][self.LINES_CLEARED]
        holes = self.data_buffer[self.index][self.HOLES]
        floor = self.data_buffer[self.index][self.FLOOR]
        floor_reward = (0 if floor < self.board.cols - 3 else floor) * 3
        height_penalty = 0
        drop_penalty = 0
        drop_reward = 0
        holes_penalty = holes ** 2
        lines_reward = lines_cleared * 10
        if efficient_drop == 0:
            drop_penalty = 4 ** 2
        else:
            drop_reward = (efficient_drop * 4) ** 2

        if current_height > last_height:
            height_penalty = (current_height if current_height - 1 > 0 else 0) ** 2

        reward = floor_reward + drop_reward + lines_reward
        penalty = height_penalty + drop_penalty + holes_penalty

        self.reward = 0.8 * self.reward + 0.2 * reward
        self.penalty = 0.8 * self.penalty + 0.2 * penalty

        self.data_buffer[self.index][self.REWARD] = self.reward
        self.data_buffer[self.index][self.PENALTY] = self.penalty
        self.data_buffer[self.index][self.REWARD_DIFF] = reward
        self.data_buffer[self.index][self.PENALTY_DIFF] = penalty
        self.data_buffer[self.index][self.FLOOR_REWARD] = floor_reward
        self.data_buffer[self.index][self.HEIGHT_PENALTY] = height_penalty
        self.data_buffer[self.index][self.DROP_PENALTY] = drop_penalty
        self.data_buffer[self.index][self.DROP_REWARD] = drop_reward
        self.data_buffer[self.index][self.HOLES_PENALTY] = holes_penalty
        self.data_buffer[self.index][self.LINES_REWARD] = lines_reward
        self.index += 1  # Track the call count

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
        x, y = piece.x, piece.y
        score = 0

        for i in range(len(shape)):
            check_piece_next = True if x == 0 else False
            check_board_next = False

            if check_piece_next is False and self.board.board[y + i, x - 1] == 1:
                check_piece_next = True

            for j in range(len(shape[i])):
                if check_piece_next is True:
                    check_piece_next = False
                    if shape[i, j] == 1:
                        score += 1

                if check_board_next is True:
                    check_board_next = False
                    if self.board.board[y + i, x + j] == 1:
                        score += 1

                if shape[i, j] == 1:
                    check_board_next = True
                elif self.board.board[y + i, x + j] == 1:
                    check_piece_next = True

            if check_board_next is True:
                j = len(shape[i])
                if j + x >= self.board.cols or self.board.board[y + i, x + j] == 1:
                    score += 1
        return score

    def flush_to_disk(self):
        """Write buffer to CSV and reset it"""
        df = pd.DataFrame(self.data_buffer, columns=Track.HEADER)
        df.to_csv(self.save_path, mode='a', header=not os.path.exists(self.save_path), index=False)

        # Reset buffer
        self.data_buffer.fill(0)
        self.index = 0

    def last_line(self):
        if self.index > 0:
            for i, title in enumerate(Track.HEADER):
                print(f"{title}={self.data_buffer[self.index][i]} ", end='')
        print("\n-----")
        if self.index > 1:
            for i, title in enumerate(Track.HEADER):
                print(f"{title}={self.data_buffer[self.index-1][i]} ", end='')
        print("\n.....")

    def close(self):
        """Ensure remaining data is written before exiting"""
        if self.index > 0:
            self.flush_to_disk()

