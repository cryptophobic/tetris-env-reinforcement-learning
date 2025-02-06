import random

import numpy as np

class TetrisEngine:
    shapes = [
        np.array([
            [1, 1, 1],
            [0, 1, 0],
        ]),
        np.array([
            [1, 1, 1, 1],
        ]),
        np.array([
            [1, 1, 1],
            [0, 0, 1],
        ]),
        np.array([
            [1, 1, 1],
            [1, 0, 0],
        ]),
        np.array([
            [1, 1, 0],
            [0, 1, 1],
        ]),
        np.array([
            [0, 1, 1],
            [1, 1, 0],
        ]),
        np.array([
            [1, 1],
            [1, 1],
        ])
    ]

    """
    Simplified Tetris game engine for RL training
    """
    def __init__(self, rows=20, cols=10):
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((rows, cols), dtype=np.int8)
        self.current_piece = None
        self.current_reward = 0
        self.lines_cleared = 0
        self.actions_performed = 0
        self.game_over = False
        self.reset()

    def reset(self):
        """Reset the game state"""
        self.board.fill(0)
        self.current_piece = self.spawn_piece()
        self.current_reward = 0
        self.lines_cleared = 0
        self.game_over = False

    def spawn_piece(self):
        """Spawn a new piece at the top of the board"""
        # return np.random.choice
        self.actions_performed += 1
        if self.current_reward > 0:
            print(self.current_reward)

        return {'shape': self.shapes[6], 'x': 3, 'y': 0}
        # return {'shape': random.choice(self.shapes), 'x': 3, 'y': 0}

    def perform_action(self, action):
        """Perform an action (0: left, 1: right, 2: rotate, 3: down, 4: drop)"""

        if action == 0:
            self.move(-1)
        elif action == 1:
            self.move(1)
        # elif action == 2:
        #     self.rotate()
        elif action == 2:
            self.fall()
        elif action == 3:
            self.hard_drop()

        if self.is_collision():
            self.merge_piece()
            self.clear_lines()
            self.current_piece = self.spawn_piece()
            if self.is_collision():  # If new piece collides, game over
                self.game_over = True
                self.actions_performed = 0

    def move(self, direction):
        """Move piece left (-1) or right (+1)"""
        self.current_piece['x'] += direction
        if self.is_collision():
            self.current_piece['x'] -= direction

    def rotate(self):
        """Rotate the piece clockwise"""
        self.current_piece['shape'] = np.rot90(self.current_piece['shape'])
        if self.is_collision():
            self.current_piece['shape'] = np.rot90(self.current_piece['shape'], -1)

    def fall(self):
        """Move piece down by one step"""
        self.current_piece['y'] += 1
        if self.is_collision():
            self.current_piece['y'] -= 1
            self.merge_piece()

    def hard_drop(self):
        """Drop the piece instantly to the lowest valid position"""
        while not self.is_collision():
            self.current_piece['y'] += 1
        self.current_piece['y'] -= 1
        self.merge_piece()

    def is_collision(self):
        """Check if the current piece collides with the board or boundaries"""
        shape = self.current_piece['shape']
        x, y = self.current_piece['x'], self.current_piece['y']
        for i in range(shape.shape[0]):
            for j in range(shape.shape[1]):
                if shape[i, j] and (y + i >= self.rows or x + j < 0 or x + j >= self.cols or self.board[y + i, x + j]):
                    return True
        return False

    def count_holes(self):
        """Count the number of holes in the board (empty spaces beneath filled blocks)."""
        holes = 0
        for col in range(self.cols):
            filled = False  # Tracks if we have encountered a filled cell
            for row in range(self.rows):
                if self.board[row, col] == 1:
                    filled = True  # Found a filled block
                elif self.board[row, col] == 0 and filled:
                    holes += 1  # Empty space below a filled block is a hole
        return holes

    def merge_piece(self):
        """Merge the current piece into the board"""
        shape = self.current_piece['shape']
        x, y = self.current_piece['x'], self.current_piece['y']
        for i in range(shape.shape[0]):
            for j in range(shape.shape[1]):
                if shape[i, j]:
                    self.board[y + i, x + j] = 1

    def clear_lines(self):
        """Clear completed lines and shift down"""
        full_rows = [i for i in range(self.rows) if np.all(self.board[i, :])]
        if len(full_rows) > 0:
            self.render()

        lines_cleared = len(full_rows)
        for row in full_rows:
            self.lines_cleared += 1
            self.board[1:row + 1, :] = self.board[:row, :]
            self.board[0, :] = 0

        if lines_cleared > 0:
            current_reward = 1 + (lines_cleared ** 2) * self.cols
            self.current_reward += current_reward

        self.current_reward -= 1

        # holes_created = self.count_holes()
        # self.current_reward = (self.lines_cleared * 10) - holes_created  # Reduce hole penalty

    def get_board_state(self):
        """Return the current board state as an observation"""
        return self.board.copy().astype(np.float32)

    def get_reward(self):
        """Return a reward based on the number of lines cleared"""
        # return self.current_reward
        # self.current_reward = np.sum(self.board == 0) / (self.rows * self.cols)
        return self.current_reward  # Reward based on empty spaces

    def is_game_over(self):
        """Check if the game is over"""
        return self.game_over

    def render(self):
        """Render the board in text mode (for debugging)"""
        print("\n".join(["".join(["⬜" if cell else "⬛" for cell in row]) for row in self.board]))
