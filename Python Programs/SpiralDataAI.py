from mynn.activators import (
    TanH,
    Softmax,
    # Sigmoid,
    # ReLU,
)
from mynn.dense import Dense
from mynn.model import Model
from mynn.cost import CategoricalCrossEntropy
from mynn.preprocess import reshape, categorize
import numpy as np
import pandas as pd
from my_decorators import Decorators

df = pd.read_csv('Data/Spiral Dataset.csv')
X = df[['Attribute 1', 'Attribute 2']].values
y = df['Answers'].values

X = reshape(X)
y = categorize(y)

network = [
    Dense(2, 40),
    TanH(),
    Dense(40, 80),
    TanH(),
    Dense(80, 100),
    TanH(),
    Dense(100, 80),
    TanH(),
    Dense(80, 40),
    TanH(),
    Dense(40, 20),
    TanH(),
    Dense(20, 10),
    TanH(),
    Dense(10, 5),
    Softmax(),
]

model = Model(network, cost_function=CategoricalCrossEntropy(), learning_rate=1e-3)
model.load('Data/Spiral Dataset saved model.json')
model.fit(X, y)
model.train = Decorators.track_time(model.train)
try:
    # model.train()
    model.train(epochs=150_000)
    accuracy = sum([np.argmax(model.predict(np.reshape(x, (1, 2, 1)))) == np.argmax(y) for x, y in zip(X, y)])
    accuracy = (accuracy / len(X)) * 100
    print(f'{accuracy = :.2f}%')
except (KeyboardInterrupt, Exception) as e:
    print(e)
finally:
    model.save(filename='Data/Spiral Dataset saved model.json')
