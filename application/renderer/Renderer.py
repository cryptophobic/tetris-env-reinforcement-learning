from application.Board import Board
from application.Piece import Piece


class Renderer:
    def __init__(self, board: Board):
        self.board = board

    def render(self, piece: Piece|None):
        raise NotImplementedError("Not implemented")
