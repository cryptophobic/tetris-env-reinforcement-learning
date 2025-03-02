import numpy as np

from application.Board import Board
from application.Perform import Perform
from application.Piece import Piece
from application.renderer.Graphics import Graphics
from application.renderer.Renderer import Renderer
from application.Track import Track
from application.renderer.Text import Text


class Engine:
    """
    Simplified Tetris game engine for RL training
    """
    def __init__(self, rows=20, cols=10, render_type="Text"):
        self.board = Board(rows=rows, cols=cols)
        self.tracker = Track(self.board)
        self.perform = Perform(self.board)
        self.renderer: Renderer = Text(self.board) if render_type == "Text" else Graphics(self.board)

        self.current_piece: Piece|None = None
        self.game_over = False

        self.reset = self.tracker.reset_wrapper(self._reset)
        self.spawn_piece = self.tracker.spawn_piece_wrapper(self._spawn_piece)
        self.set_game_over = self.tracker.set_game_over_wrapper(self._set_game_over)
        self.drop = self.tracker.drop_wrapper(self._drop)
        self.reset = self.tracker.reset_wrapper(self._reset)
        self.merge = self.tracker.merge_wrapper(self._merge)
        self.fail = self.tracker.fail_wrapper(self._fail)
        self.action = self.tracker.action_wrapper(self._action)
        self.clear_lines = self.tracker.clear_lines_wrapper(self._clear_lines)

        self.reset()

    def _reset(self) -> None:
        """Reset the game state"""
        self.board.reset_board()
        self.current_piece = self.spawn_piece()
        self.game_over = False

    # have no ide how to wrap this. Instance of wrapper stored in self.tracker = Track(self.board)
    def _spawn_piece(self) -> Piece:
        """Spawn a new piece at the top of the board"""
        self.current_piece = Piece(x=3, y=0)
        return self.current_piece

    def _set_game_over(self) -> None:
        self.game_over = True

    def _drop(self):
        return self.current_piece

    def _merge(self):
        self.board.merge_piece(self.current_piece)
        self.current_piece = None
        pass

    def _fail(self):
        pass

    def _clear_lines(self):
        return self.board.clear_lines()

    def _action(self, action):
        """Perform an action (0: left, 1: right, 2: rotate, 3: down, 4: drop)"""
        result, grounded, self.current_piece = self.perform.perform(action, self.current_piece)

        if not result:
            self.fail()

        if grounded:
            self.drop()
            self.merge()
            self.clear_lines()
            self.spawn_piece()
            if self.board.is_collision(self.current_piece):
                self.set_game_over()

            self.tracker.calculate_reward_penalty()

    def get_board_state(self):
        """Return the current board state as an observation"""
        return self.board.board.copy().astype(np.float32)

    def is_game_over(self):
        """Check if the game is over"""
        return self.game_over

    def get_reward(self) -> float:
        """Return the reward as a float"""
        return self.tracker.reward - self.tracker.penalty

    def render(self):
        """Render the game (optional for visualization)"""
        self.renderer.render(self.current_piece)
        self.tracker.last_line()

    def fall(self):
        self.perform.fall(self.current_piece)
