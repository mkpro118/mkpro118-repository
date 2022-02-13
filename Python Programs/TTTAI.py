# from mynn.model import Model
# from mynn.preprocess import (
#     categorize,
#     normalize,
# )
# import numpy as np

# import pandas as pd
# df = pd.read_csv('Data/TTTData.csv')
# features = 9
# X = np.reshape(_ := df[['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9']].values, (len(_), features, 1))
# X = normalize(X)
# y = df['m'].values
# y = categorize(y)

# model = Model.construct_from_file('Data/TTTAI Saved Model.json')
# accuracy = sum([np.argmax(model.predict(np.reshape(x, (1, features, 1)))) == np.argmax(y) for x, y in zip(X, y)])
# accuracy = (accuracy / len(X)) * 100
# print(f'{accuracy = :.2f}%')
# ###################################################################################################################

from mynn.model import Model
import numpy as np

model = Model.construct_from_file('Data/TTTAI Saved Model.json')
while True:
    board = input("Enter board: ")
    mapping = {
    'x': 1,
    'o': -1,
    '-': 0,
    }
    board = list(map(lambda x: mapping[x], list(board)))
    board = np.reshape(board, (1, 9, 1))
    row, col = divmod(np.argmax(model.predict(board)), 3)
    row, col = row + 1, col + 1
    print(f'{row = }', f'{col = }')
