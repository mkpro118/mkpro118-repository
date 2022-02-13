from mynn.dense import Dense
from mynn.activators import Sigmoid, TanH, Softmax
from mynn.cost import CategoricalCrossEntropy
from mynn.model import Model
from mynn.preprocess import train_test_split, normalize, categorize, reshape
from sklearn import datasets
import numpy as np

iris = datasets.load_iris()
X, y = np.array(iris.data), np.array(iris.target)

y = categorize(y)
X = normalize(reshape(X))

X_train, X_test, y_train, y_test = train_test_split(X, y)

network = [
    Dense(4, 36),
    TanH(),
    Dense(36, 72),
    Sigmoid(),
    Dense(72, 36),
    TanH(),
    Dense(36, 3),
    Softmax(),
]

model = Model(network, cost_function=CategoricalCrossEntropy())
model.load('Data/IRIS saved model.json')
# model = Model.construct_from_file('Data/IRIS saved model.json')
model.fit(X, y)
model.train()
# model.train(epochs=500)
accuracy = sum([np.argmax(model.predict(np.reshape(x, (1, 4, 1)))) == np.argmax(y) for x, y in zip(X, y)])
accuracy = (accuracy / len(X)) * 100
print(f'{accuracy = :.2f}%')
model.save(filename='Data/IRIS saved model.json')
