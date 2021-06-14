import numpy as np
from Chess.Piece import (Piece,
                         King,
                         Queen,
                         Rook,
                         Bishop,
                         Knight,
                         Pawn,
                         Empty)

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

board = np.full((8, 8), '  ', dtype='object')

pawns = np.array([f'{i}2' for i in 'abcdefgh'] + [f'{i}7' for i in 'abcdefgh'])
bishops = np.array(['c1', 'c8', 'f1', 'f8'])
knights = np.array(['b1', 'b8', 'g1', 'g8'])
rooks = np.array(['a1', 'a8', 'h1', 'h8'])
queens = np.array(['d1', 'd8'])
kings = np.array(['e1', 'e8'])
empty = np.array([f'{x}{i}' for x in 'abcdefgh' for i in range(3, 7)])


for position in pawns:
    file, rank = files[position[0]], ranks[position[1]]
    color = 'white' if position[1] == '2' else 'black'
    board[rank, file] = Pawn(color, position)

for position in bishops:
    file, rank = files[position[0]], ranks[position[1]]
    color = 'white' if position[1] == '1' else 'black'
    board[rank, file] = Bishop(color, position)


for position in knights:
    file, rank = files[position[0]], ranks[position[1]]
    color = 'white' if position[1] == '1' else 'black'
    board[rank, file] = Knight(color, position)


for position in rooks:
    file, rank = files[position[0]], ranks[position[1]]
    color = 'white' if position[1] == '1' else 'black'
    board[rank, file] = Rook(color, position)


for position in queens:
    file, rank = files[position[0]], ranks[position[1]]
    color = 'white' if position[1] == '1' else 'black'
    board[rank, file] = Queen(color)


for position in kings:
    file, rank = files[position[0]], ranks[position[1]]
    color = 'white' if position[1] == '1' else 'black'
    board[rank, file] = King(color)

for position in empty:
    file, rank = files[position[0]], ranks[position[1]]
    board[rank, file] = Empty(position)


board_ = ''
for row in board:
    for col in row:
        x = f'{col.get_current_position()}' if not isinstance(col, (str, np.ndarray)) else f'{col}'
        board_ += x + ' | '
    board_ += '\n' + '-' * 63
    board_ += '\n'

# print(board_)

a1_R = Pawn('white', 'd4')
# a1_R.set_current_position()
# for i in a1_R.possible_moves(board):
#     print(i)

print(a1_R.is_target_friendly(board, np.array([3, 3])))
