from dataclasses import dataclass


@dataclass
class Vec2:
    x: int
    y: int

    X = 0
    Y = 1

    def is_dirty(self) -> bool:
        return self.x != 0 or self.y != 0

    def __getitem__(self, item: int) -> int:
        if item > 1:
            raise IndexError("Out of range of 2 dimensional vector")

        return (self.x, self.y)[item]

    def __add__(self, other):
        return Vec2(self.x + other[Vec2.X], self.y + other[Vec2.Y])

    def __sub__(self, other):
        return Vec2(self.x - other[Vec2.X], self.y - other[Vec2.Y])

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y
