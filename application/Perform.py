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
        self.mapping: Dict[Action, Callable[[Piece], Tuple[bool, Piece|None]]] = {
            Action.MOVE_LEFT: self.move_left,
            Action.MOVE_RIGHT: self.move_right,
            Action.ROTATE: self.rotate,
            Action.DROP: self.drop,
            # Action.DOWN: self.fall,
        }

        self.board = board
        pass

    def move_left(self, piece: Piece) -> Tuple[bool, Piece|None]:
        return self.move(piece, -1)

    def move_right(self, piece: Piece) -> Tuple[bool, Piece|None]:
        return self.move(piece, 1)

    def move(self, piece: Piece, direction: int) -> Tuple[bool, Piece|None]:
        piece.x += direction
        success = True
        if self.board.is_collision(piece):
            piece.x -= direction
            success = False

        return success, piece

    def rotate(self, piece: Piece) -> Tuple[bool, Piece|None]:
        piece.shape = np.rot90(piece.shape)
        success = True
        if self.board.is_collision(piece):
            piece.shape = np.rot90(piece.shape, -1)
            success = False

        return success, piece

    def drop(self, piece: Piece) -> Tuple[bool, Piece|None]:
        is_collision = False
        while not is_collision:
            res, piece = self.fall(piece)
            is_collision = not res

        return True, None

    def fall(self, piece: Piece) -> Tuple[bool, Piece|None]:
        piece.y += 1
        if self.board.is_collision(piece):
            piece.y -= 1
            self.board.merge_piece(piece)
            return False, None

        return True, piece

    def perform(self, action: Action, shape: Piece) -> Tuple[bool, Piece|None]:
        return self.mapping[action](shape)

