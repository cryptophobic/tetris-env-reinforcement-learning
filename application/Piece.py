import random
import numpy as np
from application.Vectors import Vec2

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
    def __init__(self, index: int = -1, position: Vec2 = Vec2(3, 0)):
        self.shape: np.ndarray = shapes[index] if 0 <= index < len(shapes) else random.choice(shapes)
        self.position: Vec2 = position

    @property
    def x(self):
        return self.position.X

    @x.setter
    def x(self, value):
        self.position.X = value

    @property
    def y(self):
        return self.position.Y

    @y.setter
    def y(self, value):
        self.position.Y = value