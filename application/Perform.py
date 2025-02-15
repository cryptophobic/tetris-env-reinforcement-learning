from enum import Enum
from typing import Dict, Callable, Tuple
import numpy as np

from application.Board import Board
from application.Piece import Piece


class Action(Enum):
    MOVE_LEFT = 0
    MOVE_RIGHT = 1
    ROTATE = 2
    # DOWN = 2
    DROP = 3

class Perform:
    def __init__(self, board: Board):
        self.mapping: Dict[Action, Callable[[Piece], Tuple[bool, bool, Piece|None]]] = {
            Action.MOVE_LEFT: self.move_left,
            Action.MOVE_RIGHT: self.move_right,
            Action.ROTATE: self.rotate,
            Action.DROP: self.drop,
            # Action.DOWN: self.fall,
        }

        self.board = board
        pass

    def move_left(self, piece: Piece) -> Tuple[bool, bool, Piece|None]:
        return self.move(piece, -1)

    def move_right(self, piece: Piece) -> Tuple[bool, bool, Piece|None]:
        return self.move(piece, 1)

    def move(self, piece: Piece, direction: int) -> Tuple[bool, bool, Piece|None]:
        piece.x += direction
        success = True
        if self.board.is_collision(piece):
            piece.x -= direction
            success = False

        return success, False, piece

    def rotate(self, piece: Piece) -> Tuple[bool, bool, Piece|None]:
        piece.shape = np.rot90(piece.shape)
        success = True
        if self.board.is_collision(piece):
            piece.shape = np.rot90(piece.shape, -1)
            success = False

        return success, False, piece

    def drop(self, piece: Piece) -> Tuple[bool, bool, Piece|None]:
        is_collision = False
        while not is_collision:
            res, grounded, piece = self.fall(piece)
            is_collision = grounded

        return True, True, piece

    def fall(self, piece: Piece) -> Tuple[bool, bool, Piece|None]:
        piece.y += 1
        if self.board.is_collision(piece):
            piece.y -= 1
            return False, True, piece

        return True, False, piece

    def perform(self, action: Action, shape: Piece) -> Tuple[bool, bool, Piece|None]:
        return self.mapping[action](shape)

