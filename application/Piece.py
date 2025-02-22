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

colors = [
    [255, 215, 0],
    [50, 205, 50],
    [255, 255, 0],
    [34, 139, 34],
    [220, 220, 220],
    [0, 191, 255],
    [30, 144, 255],
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
        index = index if 0 <= index < len(shapes) else random.randint(0, len(shapes) - 1)
        self.shape: np.array = shapes[index]
        self.color = colors[index]
        self.x: int = x
        self.y: int = y
