from application.Piece import Piece
from application.renderer.Renderer import Renderer


class Text(Renderer):

    def render(self, piece: Piece|None):
        """Render the board in text mode (for debugging)"""
        if piece is not None:
            cols_range = range(piece.y, piece.y + piece.shape.shape[0])
            rows_range = range(piece.x, piece.x + piece.shape.shape[1])

        def render_piece(x, y):
            if piece is None:
                return "⬛"

            """Render the piece in text mode"""
            if y not in cols_range or x not in rows_range:
                return "⬛"

            y_local = y - piece.y
            x_local = x - piece.x

            return "⬜" if piece.shape[y_local, x_local] == 1 else "⬛"

        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print("\n".join(["".join(["⬜" if cell else render_piece(x, y) for x, cell in enumerate(row)]) for y, row in enumerate(self.board.board)]))
