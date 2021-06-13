import numpy as np
from Piece import Pawn, Bishop, King, Knight, Queen, Rook


class Board:
    files = {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
        'e': 4,
        'f': 5,
        'g': 6,
        'h': 7,
    }

    ranks = {
        '1': 7,
        '2': 6,
        '3': 5,
        '4': 4,
        '5': 3,
        '6': 2,
        '7': 1,
        '8': 0,
    }

    def __init__(self):
        self.board = np.empty((8, 8), dtype='object')

        pawns = np.array([f'{i}2' for i in 'abcdefgh'] + [f'{i}7' for i in 'abcdefgh'])
        bishops = np.array(['c1', 'c8', 'f1', 'f8'])
        knights = np.array(['b1', 'b8', 'g1', 'g8'])
        rooks = np.array(['a1', 'a8', 'h1', 'h8'])
        queens = np.array(['d1', 'd8'])
        kings = np.array(['e1', 'e8'])

        for position in pawns:
            file, rank = position[0], position[1]
            self.board[self.ranks[rank], self.files[file]] = 'wP' if rank == '2' else 'bP'

        for position in bishops:
            file, rank = position[0], position[1]
            self.board[self.ranks[rank], self.files[file]] = 'wB' if rank == '1' else 'bB'

        for position in knights:
            file, rank = position[0], position[1]
            self.board[self.ranks[rank], self.files[file]] = 'wN' if rank == '1' else 'bN'

        for position in rooks:
            file, rank = position[0], position[1]
            self.board[self.ranks[rank], self.files[file]] = 'wR' if rank == '1' else 'bR'

        for position in queens:
            file, rank = position[0], position[1]
            self.board[self.ranks[rank], self.files[file]] = 'wQ' if rank == '1' else 'bQ'

        for position in kings:
            file, rank = position[0], position[1]
            self.board[self.ranks[rank], self.files[file]] = 'wK' if rank == '1' else 'bK'

        filt = self.board == None
        self.board[filt] = '  '

    def __repr__(self):
        board_ = ''
        for row in self.board:
            for col in row:
                board_ += col + ' | '
            board_ += '\n' + '-' * 40
            board_ += '\n'

        return board_

if __name__ == '__main__':
    board = Board()
    print(board)
