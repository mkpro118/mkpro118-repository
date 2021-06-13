import numpy as np
# from concurrent.futures import ThreadPoolExecutor


class NeuralNet:
    def __init__(self,
                 classes=3,
                 hidden_nodes=10,
                 learning_rate=1e-3,
                 activation_function='sigmoid',
                 cost_function='cross entropy',
                 custom_activation_function=None,
                 custom_activation_function_derivative=None,
                 custom_cost_function=None,
                 custom_cost_function_derivative=None,
                 weights_hidden=None,
                 weights_output=None,
                 bias_hidden=None,
                 bias_output=None,
                 random_state=118):

        assert isinstance(classes, int), f'Number of Classes must be an {int}'
        assert isinstance(hidden_nodes, int), f'Number of Hidden Layer Nodes must be an {int}'
        assert isinstance(learning_rate, (int, float)), f'Learning Rate must be a number -> {int} or {float}'
        assert isinstance(weights_hidden, np.ndarray) or weights_hidden is None, f'Hidden Layer Weights must be a {np.ndarray} object'
        assert isinstance(weights_output, np.ndarray) or weights_output is None, f'Output Layer Weights must be a {np.ndarray} object'
        assert isinstance(bias_hidden, np.ndarray) or bias_hidden is None, f'Hidden Layer Bias must be a {np.ndarray} object'
        assert isinstance(bias_output, np.ndarray) or bias_output is None, f'Output Layer Bias must be a {np.ndarray} object'

        self.weights_hidden = weights_hidden
        self.weights_output = weights_output
        self.bias_hidden = bias_hidden
        self.bias_output = bias_output

        self.classes = classes
        self.hidden_nodes = hidden_nodes
        self.learning_rate = learning_rate

        if custom_activation_function:
            assert callable(custom_activation_function), 'Custom Activation Function is not callable'
            assert callable(custom_activation_function_derivative), 'Custom Activation Function Derivative is not callable'
            print('A Custom Activation Function has been implemented.')
            self.activation_function = custom_activation_function
            self.activation_function_derivative = custom_activation_function_derivative
        else:
            assert isinstance(activation_function, str), 'Supported Activation Functions are ReLU and Sigmoid, or specify a custom activation function using the parameter \'custom_activation_function\''
            if activation_function.lower() == 'sigmoid':
                self.activation_function = self.__sigmoid
                self.activation_function_derivative = self.__sigmoid_derivative
            elif activation_function.lower() == 'relu':
                self.activation_function = self.__relu
                self.activation_function_derivative = self.__relu_derivative
            else:
                raise ValueError(f"{activation_function} is not a supported activation function")

        if custom_cost_function:
            assert callable(custom_cost_function), 'Custom Cost Function is not callable'
            print('A Custom Cost Function has been implemented.')
            self.cost_function = custom_cost_function
            self.cost_function_derivative = custom_cost_function_derivative
        else:
            if cost_function.lower() == 'cross entropy':
                assert isinstance(cost_function, str), 'Supported Cost Functions are Cross Entropy and Mean Squared Error, or specify a custom cost function using the parameter \'custom_cost_function\''
                self.cost_function = self.__cross_entropy
            elif cost_function.lower() == 'mean squared error':
                self.cost_function = self.__mean_squared_error
            else:
                raise ValueError(f"{cost_function} is not a supported cost function")

        self.accuracy = None

        assert isinstance(random_state, int), f'Random State must be a {int} object'
        np.random.seed(random_state)

    def __str__(self):
        msg = "Model's current weights and biases :\n"
        msg += f"Hidden Layer Weights : {self.weights_hidden}\n"
        msg += f"Hidden Layer Biases : {self.bias_hidden}\n"
        msg += f"Output Layer Weights : {self.weights_output}\n"
        msg += f"Output Layer Biases : {self.bias_output}"
        return msg

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.accuracy == other.accuracy

    def __ge__(self, other):
        return self.accuracy >= other.accuracy

    def __gt__(self, other):
        return self.accuracy > other.accuracy

    def __le__(self, other):
        return self.accuracy <= other.accuracy

    def __lt__(self, other):
        return self.accuracy < other.accuracy

    def __ne__(self, other):
        return self.accuracy != other.accuracy

    def __sigmoid(self, X):
        X += 1e-14
        return 1 / (1 + np.exp(-X))

    def __sigmoid_derivative(self, X):
        return self.__sigmoid(X) * (1 - self.__sigmoid(X))

    def __relu(self, X):
        return np.maximum(0, X)

    def __relu_derivative(self, X):
        X[X <= 0] = 0
        X[X > 0] = 1
        return X

    def __cross_entropy(self, predictions):
        predictions += 1e-14
        cross_entropy = -np.sum(self.one_hot * np.log(predictions)) / self.one_hot.shape[1]
        return cross_entropy

    def __mean_squared_error(self, predictions):
        mean_squared_error = (1 / (2 * self.one_hot.shape[1])) * np.sum(np.square(self.one_hot - predictions))
        return mean_squared_error

    def __forward(self):
        unactivated_hidden_layer = self.X @ self.weights_hidden + self.bias_hidden
        activated_hidden_layer = self.activation_function(unactivated_hidden_layer)

        unactivated_output_layer = activated_hidden_layer @ self.weights_output + self.bias_output
        activated_output_layer = self.__softmax(unactivated_output_layer)

        return unactivated_hidden_layer, activated_hidden_layer, unactivated_output_layer, activated_output_layer

    def __backward(self, from_forward):
        unactivated_hidden_layer, activated_hidden_layer, unactivated_output_layer, activated_output_layer = from_forward

        dCost_dUnactivatedOutput = activated_output_layer - self.one_hot
        dUnactivatedHidden_dWO = activated_hidden_layer

        dCost_dWO = dUnactivatedHidden_dWO.T @ dCost_dUnactivatedOutput
        dCost_dBO = activated_output_layer - self.one_hot

        dCost_dActivatedHidden = dCost_dUnactivatedOutput @ self.weights_output.T
        dActivatedHidden_dUnactivatedHidden = self.activation_function_derivative(unactivated_hidden_layer)

        dCost_dWH = self.X.T @ (dActivatedHidden_dUnactivatedHidden * dCost_dActivatedHidden)
        dCost_dBH = (dCost_dUnactivatedOutput @ self.weights_output.T) * dActivatedHidden_dUnactivatedHidden

        return dCost_dWH, dCost_dBH, dCost_dWO, dCost_dBO

    def __update(self, from_backward):
        dCost_dWH, dCost_dBH, dCost_dWO, dCost_dBO = from_backward
        self.weights_hidden -= self.learning_rate * dCost_dWH
        self.bias_hidden -= self.learning_rate * dCost_dBH.sum(axis=0)
        self.weights_output -= self.learning_rate * dCost_dWO
        self.bias_output -= self.learning_rate * dCost_dBO.sum(axis=0)

    def __softmax(self, X):
        X += 1e-7
        return np.exp(X) / np.sum(np.exp(X), axis=1, keepdims=True)

    def fit(self,
            feature_set,
            labels,
            is_one_hot_encoded=False,
            num_iters=200,
            tolerance=1e-7):

        def one_hot_encode(labels):
            one_hot_encoded = np.zeros((labels.size, self.classes))
            one_hot_encoded[np.arange(labels.size), labels] = 1
            return one_hot_encoded

        def one_hot_decode(one_hot_encoded):
            labels_ = np.array([])
            for num in one_hot_encoded:
                labels_ = np.append(labels_, num.argmax())
            return labels_

        def train(iters):
            for _ in range(iters):
                from_forward = self.__forward()
                from_backward = self.__backward(from_forward)
                self.__update(from_backward)
                error = self.cost_function(from_forward[3])
                if error < tolerance:
                    break
            self.accuracy = self.score(self.X, self.y)

        assert isinstance(feature_set, np.ndarray), f'Feature Set MUST be a {np.ndarray} object'
        assert isinstance(labels, np.ndarray), f'Labels MUST be a {np.ndarray} object'
        assert isinstance(is_one_hot_encoded, bool), f'is_one_hot_encoded MUST be a {bool} object'
        assert isinstance(num_iters, int), f'Number of Iterations MUST be a {int} object'
        assert isinstance(tolerance, (int, float)), f'Error Tolerance MUST be a {float} or {int} object'

        self.X = feature_set.astype(float)
        self.y = labels if not is_one_hot_encoded else one_hot_decode(labels)
        self.one_hot = labels if is_one_hot_encoded else one_hot_encode(labels)

        self.weights_hidden = np.random.rand(self.X.shape[1], self.hidden_nodes) if not self.weights_hidden else self.weights_hidden
        self.bias_hidden = np.random.rand(self.hidden_nodes) if not self.bias_hidden else self.bias_hidden
        self.weights_output = np.random.rand(self.hidden_nodes, self.classes) if not self.weights_output else self.weights_output
        self.bias_output = np.random.rand(self.classes) if not self.bias_output else self.bias_output

        train(num_iters)

    def predict(self, X):
        assert isinstance(X, np.ndarray) and len(X.shape) == 2, f'X must be a two dimensional {np.ndarray}'
        hidden_layer_vals = self.activation_function((X @ self.weights_hidden) + self.bias_hidden)
        output_layer_vals = self.__softmax((hidden_layer_vals @ self.weights_output) + self.bias_output)
        predictions = np.array([])
        for vals in output_layer_vals:
            predictions = np.append(predictions, vals.argmax())
        return predictions.astype(int)

    def predict_proba(self, X):
        assert isinstance(X, np.ndarray) and len(X.shape) == 2, f'X must be a two dimensional {np.ndarray}'
        hidden_layer_vals = self.activation_function((X @ self.weights_hidden) + self.bias_hidden)
        output_layer_vals = self.__softmax((hidden_layer_vals @ self.weights_output) + self.bias_output)
        return output_layer_vals

    def score(self, X, y):
        y = y.ravel()
        predictions = self.predict(X)
        assert len(y) == len(predictions)
        count = (y == predictions)
        score = count.sum() / len(count)
        self.accuracy = score
        return score


if __name__ == '__main__':
    from sklearn.model_selection import train_test_split
    import pandas as pd

    df = pd.read_csv('Data/MLData.csv', index_col='ID')
    X = df[['Attribute 1', 'Attribute 2', 'Attribute 3', 'Attribute 4']].values
    y = df['Answers'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    model1 = NeuralNet(classes=4)
    model1.fit(X_train, y_train)
    print(model1.score(X_test, y_test))
    print()

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    model2 = NeuralNet(classes=4)
    model2.fit(X_train, y_train)
    print(model2.score(X_test, y_test))
    print()

    print(model2 <= model1)
