import numpy as np
from .base import CostFunction
from .cost import MeanSquaredError
from .exceptions import (UnfittedModelError,
                         InvalidNetworkError,
                         InvalidCostFunctionError,
                         InvalidLearningRateError)
from .dense import Dense
from .activation import Activation


class Model:
    """
    Objects of this class are trainable Neural Network Models

    Attributes
    ----------
        network       : list
        X             : numpy.ndarray
        Y             : numpy.ndarray
        cost_function : CostFunctions  = MeanSquaredError()
        learning_rate : float          = 0.01

    Methods
    -------
        fit(X: np.ndarray, Y: np.ndarray) -> None:
            Assigns the training input and known output sets

        train(epochs: int = 100, verbose: bool = True) -> None:
            Trains the Model based on the network and cost functions
            it was initialised with

        predict(X: np.ndarray) -> np.ndarray:
            Predcits the output from the given input
    """

    def __init__(self, network: list,
                 cost_function: CostFunction = MeanSquaredError(),
                 learning_rate: float = 0.01):
        """
        Constructs all necessary attributes for the Model object

        Parameters
        ----------
            network: list
                The network of Layers to be used for the model

            X: numpy.ndarray
                The training set of inputs

            Y: numpy.ndarray
                The training set of known outputs

            cost_function: CostFunctions  = MeanSquaredError()
                The cost function object to be used to calculate errors
                Defaults to Mean Squared Error

            learning_rate: float = 0.01
                Determines how the model performs gradient descent
                Defaults to 0.01
        """
        self.X = None
        self.Y = None
        if not isinstance(cost_function, CostFunction):
            raise InvalidCostFunctionError("Cost Function specified must be a object of derived class of mynn.base.CostFunction")
        if not isinstance(learning_rate, (float, int)):
            raise InvalidLearningRateError()
        self.network = network
        self.cost_function = cost_function
        self.learning_rate = learning_rate

    def fit(self, X: np.ndarray, Y: np.ndarray) -> None:
        """
        Fits the model with training sets

        Parameters
        ----------
            X: numpy.ndarray
                The training set of inputs

            Y: numpy.ndarray
                The training set of known outputs
        """
        if not isinstance(X, np.ndarray) or not isinstance(Y, np.ndarray):
            raise TypeError("Training sets must be a numpy.ndarray object")
        self.X = X
        self.Y = Y

    def train(self, epochs: int = 10_000, verbose: bool = True) -> None:
        """
        Trains the fitted Model based on the network and cost functions

        Parameters
        ----------
            epochs: int = 100
                Number of training iterations for the model
                Defaults to 10_000

            verbose: bool = Truw
                Displays a message showing the error after each
                training iteration
        """
        if self.X is None or self.Y is None:
            raise UnfittedModelError("""Model is not trainable without fitting the training sets.
            Use model.fit(X_train, Y_train) to fit the model with training input and output sets.""")
        for _ in range(1, epochs + 1):
            error = 0.
            for x, y in zip(self.X, self.Y):
                # Forward Propagation
                output = self.predict(x)

                # Error Calculation
                error += self.cost_function.cost(y, output)

                # Backward Propagation
                grad = self.cost_function.derivative(y, output)
                for layer in reversed(self.network):
                    grad = layer.backward(grad, self.learning_rate)

            error /= len(self.X)
            if verbose:
                print(f"{_}/{epochs}, error={error}")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """

        """
        prediction = X
        for layer in self.network:
            prediction = layer.forward(prediction)

        return prediction
