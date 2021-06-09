import numpy as np
import pandas as pd
from sklearn.utils import shuffle

np.random.seed(118)

attributes = 4
size = 1500

diff = 3

cats = np.random.randn(size, attributes) + np.array([diff, -diff, diff, -diff])
mice = np.random.randn(size, attributes) + np.array([diff, diff, -diff, diff])
dogs = np.random.randn(size, attributes) + np.array([diff, -diff, -diff, diff])
bunnies = np.random.randn(size, attributes) + np.array([-diff, diff, -diff, diff])

feature_set = np.vstack([cats, mice, dogs, bunnies])
answers = np.array([0] * size + [1] * size + [2] * size + [3] * size)

feature_set, answers = shuffle(feature_set, answers)
Id = np.arange(1, size * 4 + 1)

df = pd.DataFrame(feature_set, columns=[f'Attribute {i}' for i in range(1, attributes + 1)])

df['ID'] = Id
df['Answers'] = answers
df.set_index('ID')
df.to_csv('Data/MLData.csv', index=False)
