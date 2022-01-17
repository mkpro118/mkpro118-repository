from mynn.dense import Dense
from mynn.cost import CategoricalCrossEntropy
from mynn.activators import TanH, ReLU, Sigmoid, Softmax
from mynn.model import Model
from mynn.preprocess import categorize, normalize, train_test_split
from my_decorators import Decorators
import numpy as np
import pandas as pd

df = pd.read_csv('Data/TTTData.csv')

features = 9

X = np.reshape(_ := df[['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9']].values, (len(_), features, 1))
X = normalize(X)
y = df['m'].values
y = categorize(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, ratio=0.8)


def get_network(*args):
    return [
        Dense(9, 18),
        args[0],
        Dense(18, 36),
        args[1],
        Dense(36, 18),
        args[2],
        Dense(18, 9),
        Softmax(),
    ]


def get_cost_function():
    return CategoricalCrossEntropy()


@Decorators.memoize
def get_model_accuracy(model):
    return f'{100 * (sum([np.argmax(model.predict(np.reshape(x, (1, features, 1)))) == np.argmax(y) for x, y in zip(X_test, y_test)]) / len(X_test)) : 0.3f}'


@Decorators.track_time
def main(a1, a2, a3):
    network = get_network(a1, a2, a3)
    cost_function = get_cost_function()
    model = Model(network, cost_function=cost_function)
    # model.load('Data/CrossValidation.json')
    model.fit(X_train, y_train)
    model.train(epochs=10, verbose=False)
    return (''.join(list(map(lambda x: str(x).split()[0][0], network[1:-1:2]))), get_model_accuracy(model))


def start():
    data = []
    data.append((*main(TanH(), ReLU(), Sigmoid()), main.time))
    data.append((*main(TanH(), Sigmoid(), ReLU()), main.time))
    data.append((*main(ReLU(), TanH(), Sigmoid()), main.time))
    data.append((*main(ReLU(), Sigmoid(), TanH()), main.time))
    data.append((*main(Sigmoid(), TanH(), ReLU()), main.time))
    data.append((*main(Sigmoid(), ReLU(), TanH()), main.time))
    model, accuracy, time = [_[0] for _ in data], [_[1] for _ in data], [_[2] for _ in data]
    cvdf = pd.DataFrame({
        "Model": model,
        "Accuracy": accuracy,
        "Time": time,
        })
    print(cvdf.sort_values(['Accuracy', 'Time', 'Model'], ascending=[False, True, True]))

if __name__ == '__main__':
    start()
    start()
    start()
