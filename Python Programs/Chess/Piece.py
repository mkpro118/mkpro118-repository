import numpy as np


class Piece:
    '''
    Parent Class for all pieces
    Methods common to all pieces are defined here

    <var> name -> string : Stores the name of the piece in order to differentiate pieces

    <var> offsets -> numpy.ndarray : Stores the offsets which indiciate the very next position a piece can go to

    <var> is_sliding_piece -> bool : Sliding Pieces are : King, Queen, Rook, Bishop and Pawn
    The only non sliding piece is the Knight

    <var> files -> dict : Maps the file value from string to an integer

    <var> ranks -> dict : Maps the rank value from string to an integer
    NOTE: Mapping is done in a manner such that when the board is printed on console, the board appears from white's perspective

    <func> possible_moves : Generates all possible moves for the pieces. This is overriden by the sub classes

    <func> move : Makes the move on the board if the move is legal

    <func> is_move_legal : Determines if the selected piece can actually move to the target square according to the rules of the game

    <func> is_path_blocked : Determines if the path from the current location of the SLIDING piece to the target square is blocked by a friendly or unfriendly piece.

    <func> is_target_friendly : Determines if the target square is occupied by a friendly piece and declares the move illegal

    <func> is_target_unfriendly : Determines if the target square is occupied by a unfriendly piece.
    '''

    name = None
    offsets = None
    is_sliding_piece = True

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

    def __init__(self, color, current_position, is_sliding_piece=True):
        self.is_sliding_piece = is_sliding_piece
        self.color = color
        self.current_position_as_string = current_position
        self.current_position = np.array([ranks[current_position[0]], files[current_position[1]]])

    def get_current_position(self):
        return current_position_as_string


    def possible_moves(self, board_state):
        '''
        <param> board_state -> numpy.ndarray : Defines the state of the board at the time a move is made

        <return> -> generator object : Returns a generator of all possible moves of a piece when clicked
        '''
        pass

    def move(self, board_state, where):
        '''
        <param> board_state -> numpy.ndarray : Defines the state of the board at the time a move is made

        <param> where -> string : The location of the target square eg. 'a1' or 'h8'

        <return> None

        Makes the move on the board.
        '''
        pass

    def is_move_legal(self, board_state, where):
        '''
        <param> board_state -> numpy.ndarray : Defines the state of the board at the time a move is made

        <param> where -> string : The location of the target square eg. 'a1' or 'h8'

        Checks the following (in order):
        1. If the target square is already occupied by any friendly piece
        2. If the path to the target square is blocked by a friendl y or unfriendly piece
        3. If the target square is covered by an unfriendly piece, and allow a capture if the piece on the target square isn't the king
        (To be added at the end, the special castling rules!)
        '''
        pass

    def is_path_blocked(self, board_state, where):
        '''
        <param> board_state -> numpy.ndarray : Defines the state of the board at the time a move is made

        <param> where -> string : The location of the target square eg. 'a1' or 'h8'

        Determines if the direct path to the target square is blocked by friendly or unfriendly pieces
        '''
        pass

    def is_target_friendly(self, board_state, where):
        '''
        <param> board_state -> numpy.ndarray : Defines the state of the board at the time a move is made

        <param> where -> string : The location of the target square eg. 'a1' or 'h8'

        Determines if the target square is already occupied by a friendly piece
        '''
        pass

    def is_target_unfriendly(self, board_state, where):
        '''
        <param> board_state -> numpy.ndarray : Defines the state of the board at the time a move is made

        <param> where -> string : The location of the target square eg. 'a1' or 'h8'

        Determines if the target square is already occupied by an unfriendly piece
        '''
        pass

    def declare_illegal(self, where):
        '''
        <param> where -> string : The location of the target square eg. 'a1' or 'h8'

        Gives an alert that the move is illegal
        '''
        pass


class Rook(Piece):

    name = 'rook'

    offsets = np.array([[-1, 0],
                        [1, 0],
                        [0, -1],
                        [0, 1]])

    def __repr__(self):
        return f'{self.color} {self.name}'


class Queen(Piece):

    name = 'queen'

    offsets = np.array([[-1, 0],
                        [1, 0],
                        [0, -1],
                        [0, 1],
                        [1, 1],
                        [1, -1],
                        [-1, 1],
                        [-1, -1]])

    def __repr__(self):
        return f'{self.color} {self.name}'

    def __init__(self, color, current_position):
        super().__init__(color, current_position)


class Pawn(Piece):
    def __repr__(self):
        return f'{self.color} pawn'


class Knight(Piece):

    is_sliding_piece = False

    offsets = np.ndarray([[]])

    def __repr__(self):
        return f'{self.color} knight'


class King(Piece):
    def __repr__(self):
        return f'{self.color} king'


class Bishop(Piece):
    def __repr__(self):
        return f'{self.color} bishop'
