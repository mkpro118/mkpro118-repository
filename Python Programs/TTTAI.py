from mynn.model import Model
from mynn.preprocess import (
    categorize,
    normalize,
)
import numpy as np

import pandas as pd
df = pd.read_csv('Data/TTTData.csv')
features = 9
X = np.reshape(_ := df[['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9']].values, (len(_), features, 1))
X = normalize(X)
y = df['m'].values
y = categorize(y)

model = Model.construct_from_file('Data/prolly useless CCE model.json')
accuracy = sum([np.argmax(model.predict(np.reshape(x, (1, features, 1)))) == np.argmax(y) for x, y in zip(X, y)])
accuracy = (accuracy / len(X)) * 100
print(f'{accuracy = :.2f}%')
