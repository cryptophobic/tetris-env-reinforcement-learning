import random

import numpy as np
from stable_baselines3.common.callbacks import BaseCallback


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
        ]),
        np.array([
            [1]
        ])
    ]

    MOVE_LEFT = 0
    MOVE_RIGHT = 1
    #ROTATE = 2
    DOWN = 2
    DROP = 3

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
        self.efficient_drop = 0
        self.current_height = 0
        self.game_overs = 0
        self.floor = 0
        self.holes_created = 0
        self.game_over = False
        self.reset()

    def reset(self):
        """Reset the game state"""
        self.board.fill(0)
        self.current_piece = self.spawn_piece()
        self.lines_cleared = 0
        self.current_height = 0
        self.current_reward = 0
        self.holes_created = 0
        self.floor = 0
        self.game_over = False

    def spawn_piece(self):
        """Spawn a new piece at the top of the board"""
        self.actions_performed = 0
        self.current_reward += 1
        return {'shape': self.shapes[7], 'x': 1, 'y': 0}
        # return {'shape': random.choice(self.shapes), 'x': 3, 'y': 0}

    def perform_action(self, action):
        """Perform an action (0: left, 1: right, 2: rotate, 3: down, 4: drop)"""
        if action != 2:
            self.actions_performed += 1

        if action == 0:
            self.move(-1)
        elif action == 1:
            self.move(1)
        # elif action == 2:
        #     self.rotate()
        # elif action == 2:
        #    self.fall()
        elif action == 2:
            self.hard_drop()

        if self.is_collision():
            self.efficient_drop = self.calculate_drop_efficiency()
            self.floor = self.current_piece['x']
            self.merge_piece()
            self.clear_lines()
            self.current_piece = self.spawn_piece()
            if self.is_collision():  # If new piece collides, game over
                #self.render()
                self.game_over = True
                self.game_overs += 1
                self.current_reward -= 100
                self.holes_created = 0

            #if not self.game_over is True:
                #self.render()

                #print(self.game_overs)

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

    def calculate_drop_efficiency(self):
        """Calculate the drop efficiency based on available space left and right."""
        x, y = self.current_piece['x'], self.current_piece['y']
        shape_width = self.current_piece['shape'].shape[1]

        space_left = x > 0 and self.board[y, x - 1] == 0
        space_right = x + shape_width < self.cols and self.board[y, x + shape_width] == 0

        if space_left and space_right:
            return 0  # Space available on both sides
        elif space_left or space_right:
            return 1  # Space available on one side only
        else:
            return 2  # No space on either side

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
        #if len(full_rows) > 0 or efficient_drop > 1:
        #    self.render()

        self.lines_cleared += len(full_rows)
        for row in full_rows:
            self.board[1:row + 1, :] = self.board[:row, :]
            self.board[0, :] = 0

        #if lines_cleared > 0:
        #    current_reward = 1 + (lines_cleared ** 2) * self.cols
        #    self.current_reward += current_reward

        #self.current_reward -= 1
        self.current_height = self.calculate_max_height()
        self.holes_created = self.count_holes()


    def calculate_max_height(self):
        """Calculate the maximum height of stacked pieces."""
        for row in range(self.rows):
            if np.any(self.board[row, :]):  # If any block exists in the row
                return self.rows - row  # Height from the bottom
        return 0  # If board is empty

    def get_board_state(self):
        """Return the current board state as an observation"""
        return self.board.copy().astype(np.float32)

    def get_reward_(self):
        """Return a reward based on the number of lines cleared"""
        height_penalty = self.current_height * 3
        action_penalty = max(0, self.actions_performed - 3)  # Only penalize if more than 5 actions
        self.current_reward = ((self.lines_cleared * 10) - self.holes_created) + self.efficient_drop - height_penalty - action_penalty# Reduce hole penalty

        return self.current_reward

    def get_reward(self):
        """Return a reward based on the number of lines cleared"""
        height_penalty = (self.current_height if self.current_height - 1 > 0 else 0) * 2
        action_penalty = max(0, self.actions_performed - 3)  # Only penalize if more than 5 actions

        # ✅ Weighted average to balance current reward with past rewards
        self.current_reward = 0.8 * self.current_reward + 0.2 * (
                    (self.lines_cleared * 10) - self.holes_created - height_penalty - action_penalty + self.efficient_drop - ((self.rows - 1 - self.floor) * 2))

        #print(f"height_penalty: {height_penalty}")
        #print(f"current_height: {self.current_height}")
        #print(f"actions_performed: {self.actions_performed}")
        #print(f"lines_cleared: {self.lines_cleared}")
        #print(f"holes_created: {self.holes_created}")
        #print(f"efficient_drop: {self.efficient_drop}")

        return self.current_reward

    def is_game_over(self):
        """Check if the game is over"""
        return self.game_over

    def render(self):
        """Render the board in text mode (for debugging)"""
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

        def render_piece(x, y):
            """Render the piece in text mode"""
            self.board[y, x] = 1
            collision = self.is_collision()
            self.board[y, x] = 0

            return "⬜⬜" if collision else "⬛⬛"


        print("\n".join(["".join(["⬜⬜" if cell else render_piece(x, y) for x, cell in enumerate(row)]) for y, row in enumerate(self.board)]))
        print(self.get_reward())

class CustomCallback(BaseCallback):
    def __init__(self, env, check_freq=8192, verbose=1):
        super(CustomCallback, self).__init__(verbose)
        self.env = env
        self.check_freq = check_freq
        self.step_counter = 0

    def _on_step(self) -> bool:
        self.step_counter += 1
        if self.step_counter % self.check_freq == 0:
            print(f"🔹 Custom event triggered at step {self.step_counter}")
            # Access the TetrisEnv or TetrisEngine instance here
            # 🔥 Correct way to access the original environment
            if hasattr(self.env, "env"):
                tetris_engine = self.env.env.engine  # Access the wrapped environment
            else:
                tetris_engine = self.env.engine  # Use directly if not wrapped

            # Append-adds at last
            file1 = open("deaths.cnt", "a")  # append mode
            file1.write(f"{str(tetris_engine.game_overs)}\n")
            file1.close()

            print(f"Total game overs in last {self.check_freq} Deaths: {tetris_engine.game_overs}")
            tetris_engine.game_overs = 0
            #print("Board State:\n", tetris_engine.get_board_state())
        return True
