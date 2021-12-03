from dense import Dense
from model import Model
from activators import TanH
from cost import MeanSquaredError
import numpy as np

X = np.reshape([[0, 0], [1, 0], [0, 1], [1, 1], ], (4, 2, 1,))
Y = np.reshape([[0, ], [1, ], [1, ], [1, ], ], (4, 1, 1,))

network = [
    Dense(2, 5),
    TanH(),
    Dense(5, 4),
    TanH(),
    Dense(4, 1),
    TanH(),
]

model = Model(network, cost_function=MeanSquaredError(),
              learning_rate=0.05)

model.fit(X, Y)
model.train(verbose=True)  # False if you don't want the decrease in error displayed
print(model.predict(np.reshape([[0, 0, ], ], (1, 2, 1)))[0, 0, 0])
print(model.predict(np.reshape([[0, 1, ], ], (1, 2, 1)))[0, 0, 0])
print(model.predict(np.reshape([[1, 0, ], ], (1, 2, 1)))[0, 0, 0])
print(model.predict(np.reshape([[1, 1, ], ], (1, 2, 1)))[0, 0, 0])
