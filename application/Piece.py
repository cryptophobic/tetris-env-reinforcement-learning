import random
import numpy as np

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
]

class Piece:

    ANY_TETRIMINO = -1
    T_TETRIMINO = 0
    I_TETRIMINO = 1
    J_TETRIMINO = 2
    L_TETRIMINO = 3
    Z_TETRIMINO = 4
    S_TETRIMINO = 5
    O_TETRIMINO = 6

    def __init__(self, x: int = 3, y: int = 0, index: int = ANY_TETRIMINO):
        self.shape: np.ndarray = shapes[index] if 0 <= index < len(shapes) else random.choice(shapes)
        self.x: int = x
        self.y: int = y
