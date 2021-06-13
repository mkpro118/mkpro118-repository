import numpy as np

class Piece:

    is_sliding_piece = True
    original_location = None
    color = 'white'
    starting_position = 'd1'

    def possibleMoves():
        pass


class Rook(Piece):
    def __repr__(self):
        return f'{self.color} rook'


class Queen(Piece):
    def __repr__(self):
        return f'{self.color} queen'


class Pawn(Piece):
    def __repr__(self):
        return f'{self.color} pawn'

class Knight(Piece):

    isSlidingPiece = False

    def __repr__(self):
        return f'{self.color} knight'


class King(Piece):
    def __repr__(self):
        return f'{self.color} king'


class Bishop(Piece):
    def __repr__(self):
        return f'{self.color} bishop'
