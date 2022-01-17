import numpy as np
from time import perf_counter as pc
import asyncio
from sklearn.model_selection import train_test_split
import pandas as pd
import warnings
# from matplotlib import pyplot as plt

np.random.seed(118)


class NeuralNetworkMultiClassifier:
    def __init__(self, hidden_nodes=5, output_answers=4, learning_rate=2.5e-4):
        self.learning_rate = learning_rate
        self.weights_output, self.weights_hidden, self.bias_hidden, self.bias_output = [None] * 4
        self.hidden_nodes = hidden_nodes
        self.output_answers = output_answers

    def _sigmoid(self, x: np.ndarray) -> np.ndarray:
        assert isinstance(x, np.ndarray)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            result = 1. / (1. + np.exp(-x))
        return result

    def _sigmoid_derivative(self, x: np.ndarray) -> np.ndarray:
        assert isinstance(x, np.ndarray)
        return self._sigmoid(x) * (1 - self._sigmoid(x))

    def _softmax(self, x: np.ndarray) -> np.ndarray:
        assert isinstance(x, np.ndarray)
        X = x - np.max(x, axis=1, keepdims=True)
        expx = np.exp(X)
        return expx / expx.sum(axis=1, keepdims=True)

    def fit(self, X: np.ndarray, y: np.ndarray,
            num_iters: int = 300, threads: int = 4) -> None:
        async def _train(iters: int) -> None:
            # print('training')
            for _ in range(iters):
                # Feed Forward Process

                # phase 1
                z_hidden = X @ self.weights_hidden + self.bias_hidden
                a_hidden = self._sigmoid(z_hidden)

                # phase 2
                z_output = a_hidden @ self.weights_output + self.bias_output
                a_output = self._softmax(z_output)

                # Back Propagation
                # phase 1

                dcost_dz_output = a_output - self.one_hot_encoding
                dz_output_dweights_output = a_hidden

                dcost_weights_output = dz_output_dweights_output.T @ dcost_dz_output

                dcost_bias_output = dcost_dz_output

                # phase 2

                dz_output_da_hidden = self.weights_output
                dcost_da_hidden = dcost_dz_output @ dz_output_da_hidden.T
                da_hidden_dz_hidden = self._sigmoid_derivative(z_hidden)

                dcost_weights_hidden = X.T @ (da_hidden_dz_hidden * dcost_da_hidden)
                dcost_bias_hidden = dcost_da_hidden * da_hidden_dz_hidden

                # update weights and bias

                self.weights_hidden -= self.learning_rate * dcost_weights_hidden
                self.bias_hidden -= self.learning_rate * dcost_bias_hidden.sum(axis=0)

                self.weights_output -= self.learning_rate * dcost_weights_output
                self.bias_output -= self.learning_rate * dcost_bias_output.sum(axis=0)

            await asyncio.sleep(1e-7)

        async def main():
            iters = [_train(num_iters // threads)] * threads
            await asyncio.gather(*iters)

        assert isinstance(X, np.ndarray) and isinstance(y, np.ndarray)
        self.one_hot_encoding = np.zeros((X.shape[0], self.output_answers))
        self.one_hot_encoding[np.arange(y.size), y] = 1
        self.examples = X.shape[0]
        self.attributes = X.shape[1]
        self.weights_hidden = np.random.rand(self.attributes, self.hidden_nodes)
        self.bias_hidden = np.random.rand(self.hidden_nodes)
        self.weights_output = np.random.rand(self.hidden_nodes, self.output_answers)
        self.bias_output = np.random.rand(self.output_answers)

        asyncio.run(main())

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        assert isinstance(X_test, np.ndarray)
        X_test = self._sigmoid(X_test @ self.weights_hidden + self.bias_hidden)
        predictions = np.array([])
        results = self._softmax(X_test @ self.weights_output + self.bias_output)
        for num in results:
            predictions = np.append(predictions, num.argmax())
        return predictions.astype(int)

    def predict_proba(self, X_test: np.ndarray) -> np.ndarray:
        assert isinstance(X_test, np.ndarray)
        X_test = self._sigmoid(X_test @ self.weights_hidden + self.bias_hidden)
        results = self._softmax(X_test @ self.weights_output + self.bias_output)
        return results

    def score(self, X_test: np.ndarray, y_test: np.ndarray) -> float:
        assert isinstance(X_test, np.ndarray) and isinstance(y_test, np.ndarray)
        y_test = y_test.ravel()
        y_pred = self.predict(X_test)
        assert len(y_test) == len(y_pred)
        count = (y_test == y_pred)
        result = count.sum() / len(count)
        return result


if __name__ == '__main__':
    # # A Good Dataset
    # # From a file of randomly generated numbers
    print('Time taken to create the training and test datasets...', end=' ')
    t1 = pc()
    df = pd.read_csv('Data/MLData.csv', index_col='ID')
    X = df[['Attribute 1', 'Attribute 2', 'Attribute 3', 'Attribute 4']].values
    y = df['Answers'].values

    # # Linear Dataset
    # df = pd.read_csv('Data/Linear Dataset.csv')
    # X = df[['x', 'y']].values
    # y = df['color'].values

    # # Quadratic Dataset
    # df = pd.read_csv('Data/Quadratic Dataset.csv')
    # X = df[['x', 'y']].values
    # y = df['color'].values

    # # A Horrible  Dataset
    # # From https://cs231n.github.io/neural-networks-case-study/
    # N = 100  # number of points per class
    # D = 2  # dimensionality
    # K = 4  # number of classes
    # X = np.zeros((N * K, D))  # data matrix (each row = single example)
    # y = np.zeros(N * K, dtype='uint8')  # class labels
    # for j in range(K):
    #     ix = range(N * j, N * (j + 1))
    #     r = np.linspace(0.0, 1, N)  # radius
    #     t = np.linspace(j * 4, (j + 1) * 4, N) + np.random.randn(N) * 0.2  # theta
    #     X[ix] = np.c_[r * np.sin(t), r * np.cos(t)]
    #     y[ix] = j

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=92)
    print(round(pc() - t1, 4), 'seconds', end='\n\n')

    print('Time taken to train the model...', end=' ')
    model = NeuralNetworkMultiClassifier(output_answers=4)
    t1 = pc()
    model.fit(X_train, y_train)
    print(round(pc() - t1, 4), 'seconds', end='\n\n')

    print('Time taken to find the accuracy of the model...', end=' ')
    t1 = pc()
    accuracy = round(model.score(X_test, y_test) * 100, 5)
    print(round(pc() - t1, 4), 'seconds')
    print(f'Accuracy: {accuracy} %\n')

    print('Time taken to make predictions...', end=' ')
    t1 = pc()
    predictions = model.predict(X_test)
    print(round(pc() - t1, 4), 'seconds')
    print('Predictions: ', predictions, sep=' ' * 3)
    print('Acutal Values: ', y_test)

# new class
