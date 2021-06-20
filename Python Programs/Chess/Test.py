from time import sleep
from Board import Board
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('test.log')
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

board = Board()
board = board.board

# board_ = ''
# for row in board:
#     for col in row:
#         x = f'{col.get_current_position()}' if not isinstance(col, (str, np.ndarray)) else f'{col}'
#         board_ += x + ' | '
#     board_ += '\n' + '-' * 63
#     board_ += '\n'

# print(board_)

# print(k.is_sliding_piece)
# board[6, 0] = Empty('a2')

# Moving the e2 Pawn to e4
k = board[6, 4]
k.move(board, 'e4')
logger.info(board)
logger.info('')

sleep(1.5)

# Moving the f7 Pawn to f6
k = board[1, 5]
k.move(board, 'f6')
logger.info(board)
logger.info('')

sleep(1.5)

# Moving the d2 Pawn to d4
k = board[6, 3]
k.move(board, 'd4')
logger.info(board)
logger.info('')

sleep(1.5)

# Moving the g7 Pawn to g5
k = board[1, 6]
k.move(board, 'g5')
logger.info(board)
logger.info('')

sleep(1.5)

# Moving the d1 Queen to h5
k = board[7, 3]
k.move(board, 'h5')

logger.info(board)
logger.info('')
