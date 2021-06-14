import numpy as np
from Piece import (Pawn,
                   Bishop,
                   Knight,
                   Rook,
                   Queen,
                   King,
                   Empty)


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
        self.board = np.full((8, 8), '  ', dtype='object')

        pawns = np.array([f'{i}2' for i in 'abcdefgh'] + [f'{i}7' for i in 'abcdefgh'])
        bishops = np.array(['c1', 'c8', 'f1', 'f8'])
        knights = np.array(['b1', 'b8', 'g1', 'g8'])
        rooks = np.array(['a1', 'a8', 'h1', 'h8'])
        queens = np.array(['d1', 'd8'])
        kings = np.array(['e1', 'e8'])
        empty = np.array([f'{x}{i}' for x in 'abcdefgh' for i in range(3, 7)])

        for position in pawns:
            file, rank = self.files[position[0]], self.ranks[position[1]]
            color = 'white' if position[1] == '2' else 'black'
            self.board[rank, file] = Pawn(color, position)

        for position in bishops:
            file, rank = self.files[position[0]], self.ranks[position[1]]
            color = 'white' if position[1] == '1' else 'black'
            self.board[rank, file] = Bishop(color, position)

        for position in knights:
            file, rank = self.files[position[0]], self.ranks[position[1]]
            color = 'white' if position[1] == '1' else 'black'
            self.board[rank, file] = Knight(color, position)

        for position in rooks:
            file, rank = self.files[position[0]], self.ranks[position[1]]
            color = 'white' if position[1] == '1' else 'black'
            self.board[rank, file] = Rook(color, position)

        for position in queens:
            file, rank = self.files[position[0]], self.ranks[position[1]]
            color = 'white' if position[1] == '1' else 'black'
            self.board[rank, file] = Queen(color)

        for position in kings:
            file, rank = self.files[position[0]], self.ranks[position[1]]
            color = 'white' if position[1] == '1' else 'black'
            self.board[rank, file] = King(color)

        for position in empty:
            file, rank = self.files[position[0]], self.ranks[position[1]]
            self.board[rank, file] = Empty(position)

    def __repr__(self):
        board_ = '-' * 41 + '\n'
        for row in self.board:
            board_ += '| '
            for col in row:
                board_ += str(col) + ' | '
            board_ += '\n' + '-' * 41
            board_ += '\n'

        return board_


if __name__ == '__main__':
    board = Board()
    print(board)
