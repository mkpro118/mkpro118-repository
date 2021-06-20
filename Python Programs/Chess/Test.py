from Board import Board
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('test.log')
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

board = Board()


def moves():
    k = ['e2', 'e4', 'e7', 'e5', 'b1', 'c3', 'b8', 'c6',
         'f1', 'c4', 'f8', 'c5', 'd1', 'g4', 'd8', 'f6',
         'c3', 'd5', 'f6', 'f2', 'e1', 'd1', 'g7', 'g6',
         'g1', 'h3', 'f2', 'd4', 'd2', 'd3', 'h7', 'h5',
         'g4', 'f3', 'g8', 'f6', 'c2', 'c3', 'f6', 'd5',
         'c3', 'd4', 'e5', 'd4', 'e4', 'd5', 'c6', 'a5',
         'h1', 'e1', 'e8', 'f8', 'e1', 'f1', 'a5', 'c4',
         'f3', 'f7']
    yield from k


move = moves()

while True:
    try:
        k = board.getPiece(next(move))
        k.move(board.board, next(move))
        logger.info(board)
        logger.info('')
    except StopIteration:
        break
