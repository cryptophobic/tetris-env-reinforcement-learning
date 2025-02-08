from application.tetris_env import TetrisEnv

env = TetrisEnv()
self = env.engine
self.reset()
self.current_piece['x'] = 0
# piece = self.current_piece
# print(piece)
# shape = piece['shape']
# x, y = piece['x'], piece['y']
# env.engine.board[y, x - 1] = 1
# env.engine.board[y, x + 3] = 1
# env.engine.board[y+1, x - 1] = 1
# env.engine.board[y+1, x] = 1
# env.engine.board[y+1, x+2] = 1
# env.engine.board[y+1, x+3] = 1


score = 0


def calculate_neighbours(self):
    """Calculate how well a piece is placed based on neighboring blocks."""
    piece = self.current_piece
    shape, x, y = piece['shape'], piece['x'], piece['y']
    score = 0

    for i in range(shape.shape[0]):
        for j in range(shape.shape[1]):
            if shape[i, j] == 1:
                # Check left neighbor
                if x + j > 0 and self.board[y + i, x + j - 1] == 1:
                    score += 1
                # Check right neighbor
                if x + j < self.cols - 1 and self.board[y + i, x + j + 1] == 1:
                    score += 1
                # Check bottom neighbor
                if y + i < self.rows - 1 and self.board[y + i + 1, x + j] == 1:
                    score += 1
    return score


def calculate_neighbors(self):
    """Calculate how well a piece is placed based on neighboring blocks."""
    piece = self.current_piece
    shape = piece['shape']
    x, y = piece['x'], piece['y']
    score = 0

    for i in range(len(shape)):
        check_piece_next = True if x == 0 else False
        check_board_next = False

        if check_piece_next is False and self.board[y + i, x - 1] == 1:
            check_piece_next = True

        for j in range(len(shape[i])):
            if check_piece_next is True:
                check_piece_next = False
                if shape[i, j] == 1:
                    score += 1

            if check_board_next is True:
                check_board_next = False
                if self.board[y + i, x + j] == 1:
                    score += 1

            if shape[i, j] == 1:
                check_board_next = True
            elif self.board[y + i, x + j] == 1:
                check_piece_next = True

        if check_board_next is True:
            j = len(shape[i])
            if j + x >= self.cols or self.board[y + i, x + j] == 1:
                score += 1
    return score

print(calculate_neighbors(self))
