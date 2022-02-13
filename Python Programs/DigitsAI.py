from mynn.dense import Dense
from mynn.activators import Sigmoid, ReLU, TanH, Softmax
from mynn.cost import CategoricalCrossEntropy
from mynn.model import Model
from mynn.preprocess import train_test_split, normalize, categorize, reshape
from sklearn import datasets
import numpy as np
from my_decorators import Decorators

# load dataset

digits = datasets.load_digits()
data, targets = digits.data, digits.target

# array-fy the data and target

X, y = np.array(data), np.array(targets)

y = categorize(y)  # one hot encode
X = normalize(reshape(X))  # have data between -1 and 1

X_train, X_test, y_train, y_test = train_test_split(X, y)

network = [
    Dense(64, 128),
    TanH(),
    Dense(128, 256),
    TanH(),
    Dense(256, 128),
    TanH(),
    Dense(128, 10),
    Softmax(),
]

model = Model(network, cost_function=CategoricalCrossEntropy())
model.load('Data/DIGITS saved model.json')
# model = Model.construct_from_file('Data/DIGITS saved model.json')
# model.fit(X_train, y_train)
# model.train = Decorators.track_memory(Decorators.track_time(model.train))
try:
    # model.train()
    # model.train(epochs=2500)
    accuracy = sum([np.argmax(model.predict(np.reshape(x, (1, 64, 1)))) == np.argmax(y) for x, y in zip(X, y)])
    accuracy = (accuracy / len(X)) * 100
    print(f'{accuracy = :.2f}%')
except (KeyboardInterrupt, Exception) as e:
    print('Error occured')
    print(e)
finally:
    # model.save(filename='Data/DIGITS saved model.json')
    pass
