import numpy as np


class Piece:
    '''
    Parent Class for all pieces
    Methods common to all pieces are defined here

    <var> name -> string : Stores the name of the piece in order to differentiate pieces

    <var> offsets -> numpy.ndarray : Stores the offsets which indiciate the very next position a piece can go to

    <var> is_sliding_piece -> bool : Sliding Pieces are : Queen, Rook and Bishop
    The non sliding pieces are Pawn, Knight, King

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
        '''
        <param> color -> string : 'white' or 'black' indicating the color of the piece

        <param> current_position -> string : The location of the square where the piece must be placed eg. 'a1' or 'h8'

        <optional param> is_sliding_piece -> bool : True indicates that the piece is a sliding piece. Should be False for Knights only
        '''
        assert isinstance(color, str), 'Color values can be either \'white\' or \'black\''
        assert isinstance(current_position, str), 'Position of the square must be in the standard algebraic notation for Chess, eg. \'A1\' or \'h8\''
        assert all([len(current_position) == 2,
                    current_position[0] in self.files,
                    current_position[1] in self.ranks]), 'Invalid Square'
        assert isinstance(is_sliding_piece, bool), 'is_sliding_piece must be a True or False value'
        self.is_sliding_piece = is_sliding_piece
        self.color = color
        self.current_position_as_string = current_position.lower()
        self.current_position = np.array([self.ranks[current_position[1]], self.files[current_position[0]]])

    def get_current_position_as_string(self):
        '''
        <return> -> string : The current location of the piece as a string, eg. 'a1' or 'h8'
        '''
        return self.current_position_as_string

    def get_current_position(self):
        '''
        <return> -> numpy.ndarray : The current location of the piece as an element of a numpy array, eg. array([1 0]) or array([3 4])
        NOTE : The first element is the rank, the second element in the file
        '''
        return self.current_position

    def set_current_position(self, target_position):
        '''
        <param> target_position -> string : The co-ordinates of the target square
        '''
        rank, file = self.ranks[target_position[1]], self.files[target_position[0]]
        self.current_position = np.array([rank, file])

    def possible_moves(self, board):
        '''
        <param> board -> np.ndarray : Shows the board

        <return> -> generator object : Returns a generator of all possible moves of a piece when clicked
        '''
        possible_moves = []
        for offset in self.offsets:
            position = self.get_current_position()
            rank, file = position[0], position[1]
            while True:
                rank_offset, file_offset = offset[0], offset[1]
                rank_possible = rank + rank_offset
                file_possible = file + file_offset
                try:
                    _ = board[rank_possible, file_possible]
                    assert not rank_possible < 0
                    assert not file_possible < 0

                except IndexError:
                    break
                except AssertionError:
                    break
                else:
                    possible_moves.append([rank_possible, file_possible])
                    rank = rank_possible
                    file = file_possible
                finally:
                    if self.name == 'KING' or self.name == 'PAWN' or self.name == 'KNIGHT':
                        break

        yield from possible_moves

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
    '''
    The white rooks start on squares a1 and h1, while the black rooks start on a8 and h8.
    The rook moves horizontally or vertically, through any number of unoccupied squares.
    The rook cannot jump over pieces.
    The rook also participates, with the king, in a special move called castling.

    <var> name -> string : Name of the piece

    <var> offsets -> np.ndarray : Offsets indicate which direction the Rook can move in
    '''

    name = 'ROOK'

    offsets = np.array([[-1, 0],
                        [1, 0],
                        [0, -1],
                        [0, 1]])

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f'{self.color[0]}{self.name[0]}'


class Queen(Piece):
    '''
    The white queen start on squares d1, while the black queen start on d8.
    The queen can be moved any number of unoccupied squares in a straight line vertically,
    horizontally, or diagonally, thus combining the moves of the rook and bishop


    <var> name -> string : Name of the piece

    <var> offsets -> np.ndarray : Offsets indicate which direction the Queen can move in
    '''

    name = 'QUEEN'

    offsets = np.array([[-1, 0],
                        [1, 0],
                        [0, -1],
                        [0, 1],
                        [1, 1],
                        [1, -1],
                        [-1, 1],
                        [-1, -1]])

    def __init__(self, color):
        position = 'd1' if color == 'white' else 'd8'
        super().__init__(color, position)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f'{self.color[0]}{self.name[0]}'


class Pawn(Piece):
    '''
    The white pawns start on the second rank
    Unlike the other pieces, pawns cannot move backwards.
    Normally a pawn moves by advancing a single square, but the first time a pawn moves, it has the option of advancing two squares.
    Pawns may not use the initial two-square advance to jump over an occupied square, or to capture.
    Any piece immediately in front of a pawn, friend or foe, blocks its advance.

    <var> name -> string : Name of the piece

    <var> offsets -> np.ndarray : Offsets indicate which direction the Rook can move in
    '''

    name = 'PAWN'

    is_sliding_piece = False

    def __init__(self, color, current_position):
        super().__init__(color, current_position)
        self.has_moved = False
        if color == 'white':
            if self.get_current_position_as_string()[1] != '2':
                self.offsets = np.array([[-1, 0],
                                         [-1, 1],
                                         [-1, -1]])
            else:
                self.offsets = np.array([[-1, 0],
                                         [-1, 1],
                                         [-1, -1],
                                         [-2, 0]])
        else:
            if self.get_current_position_as_string()[1] != '7':
                self.offsets = np.array([[1, 0],
                                         [1, 1],
                                         [1, -1]])
            else:
                self.offsets = np.array([[1, 0],
                                         [1, 1],
                                         [1, -1],
                                         [2, 0]])

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f'{self.color[0]}{self.name[0]}'


class Knight(Piece):
    '''
    The white knight start on squares b1 and g1, while the black knight start on b8 and g8.
    Compared to other chess pieces, the knight's movement is unique: it may move two squares vertically and one square horizontally,
    or two squares horizontally and one square vertically (with both forming the shape of an L).
    This way, a knight can have a maximum of 8 moves. While moving, the knight can jump over pieces to reach its destination.

    <var> name -> string : Name of the piece

    <var> offsets -> np.ndarray : Offsets indicate which direction the Rook can move in
    '''

    is_sliding_piece = False
    name = 'KNIGHT'
    offsets = np.array([[1, 2],
                        [2, 1],
                        [-1, 2],
                        [-2, -1],
                        [-1, -2],
                        [-2, 1],
                        [1, -2],
                        [2, -1]])

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f'{self.color[0]}{self.name[1]}'


class King(Piece):
    '''
    The white king start on squares e1, while the black king start on e8.
    A king can move one square in any direction (horizontally, vertically, or diagonally),
    unless the square is already occupied by a friendly piece, or the move would place the king in check.
    As a result, opposing kings may never occupy adjacent squares (see opposition) to give check,
    as that would put the moving king in check as well.
    However, the king can give discovered check by unblocking a bishop, rook, or queen.
    The king is also involved in the special move of castling.

    <var> name -> string : Name of the piece

    <var> offsets -> np.ndarray : Offsets indicate which direction the Rook can move in
    '''

    name = 'KING'

    is_sliding_piece = False

    offsets = np.array([[-1, 0],
                        [1, 0],
                        [0, -1],
                        [0, 1],
                        [1, 1],
                        [1, -1],
                        [-1, 1],
                        [-1, -1]])

    def __init__(self, color):
        position = 'e1' if color == 'white' else 'e8'
        super().__init__(color, position)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f'{self.color[0]}{self.name[0]}'


class Bishop(Piece):
    '''
    The white bishops start on squares c1 and f1, while the black bishops start on c8 and f8.
    The bishop has no restrictions in distance for each move, but is limited to diagonal movement.
    Bishops, like all other pieces except the knight, cannot jump over other pieces.

    <var> name -> string : Name of the piece

    <var> offsets -> np.ndarray : Offsets indicate which direction the Rook can move in
    '''

    name = 'BISHOP'

    offsets = np.array([[1, 1],
                        [-1, 1],
                        [1, -1],
                        [-1, -1]])

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f'{self.color[0]}{self.name[0]}'
