from Board import Board
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('test2.log')
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

board = Board()


def moves():
    k = ['d2', 'd4', 'd7', 'd5', 'e2', 'e4', 'd5', 'e4',
         'f2', 'f3', 'e4', 'f3', 'd1', 'f3', 'd8', 'd4',
         'b1', 'c3', 'g8', 'f6', 'c1', 'e3', 'd4', 'b4',
         'a1', 'd1', 'c8', 'g4', 'c3', 'b5', 'g4', 'f3',
         'b5', 'c7']
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
