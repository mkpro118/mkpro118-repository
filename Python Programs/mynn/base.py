import numpy as np
import typing  # type hinting only


class Layer:
    """
    Base class for creating Neural Network's Layers

    Attributes
    ----------
    input  : numpy.ndarray
        The input matrix to be used by the layer

    output : numpy.ndarray
        The output matrix produced by the layer

    Methods
    -------
    forward(input: numpy.ndarray) -> numpy.ndarray:
        Passes the output to the next layer in forward propagation

    backward(output_gradient: numpy.ndarray,
              learning_rate: float = 0.1) -> numpy.ndarray:
        Passes the output to the previous layer in backward propagation
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the Layer object
        """
        self.input = None
        self.output = None

    def forward(self, input: np.ndarray) -> np.ndarray:
        """
        Carries out the forward propagation from this Layer to the next
        Does not check for the presence of the next layer.

        Parameters
        ----------
            input: numpy.ndarray

        Returns
        -------
            a `numpy.ndarray` of the result of f(X) = WX + B
        """
        pass

    def backward(self, output_gradient: np.ndarray,
                 learning_rate: float = 0.1) -> np.ndarray:
        """
        Carries out the backward propagation from this Layer to the previous.
        Updates this layers weights and biases, according to the learning rate
        Does not check for the presence of the previous layer.

        Parameters
        ----------
            output_gradient: numpy.ndarray
            learning_rate  : float

        Returns
        -------
            a ``numpy.ndarray`` of the result of derivative of error w.r.t the Input to this layer

        Alorithm
        --------
            Output Gradient is the derivative of the error w.r.t the input of the next layer
            Let's denote that as dE / dY.

            The first objective here is to calculate the derivative of the error w.r.t the input of this layer
            Let's denote that as dE / dX.
            By matrix manipulation, the derivative of the error w.r.t the input of this layer is equal to
            the matrix multiplication (``numpy.dot``) of the transpose of the weights matrix and,
            the derivative of the error w.r.t the input of the next layer.
            So, dE / dX = W' @ (dE / dY).

            The second objective is to update the weights and biases.
            Weights:
                This is achieved by subtracting the product of the learning rate and
                the matrix product of dE / dY and the transpose of the input matrix.
            Biases:
                This is achieved by subtracting the product of the learning rate and
                the matrix dE / dY.

        NOTE
        ----
            Using both ``numpy.dot`` and the ``@`` operator are okay here
            because both work the same for 2D numpy arrays.
        """
        pass


class CostFunction:
    """
    Base Class for Cost Functions

    Attributes
    ----------
        None

    Methods
    -------
        cost(y_true: numpy.ndarray,
             y_pred: numpy.ndarray) -> numpy.ndarray:
             Calculates the error between the true (y_true)
             and predicted (y_pred) values

        derivative(y_true: numpy.ndarray,
                   y_pred: numpy.ndarray) -> numpy.ndarray:
            Calculates the derivative of the error between
            the true(y_true) and predicted(y_pred) values
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the CostFunctions object
        """
        pass

    def cost(y_true: np.ndarray,
             y_pred: np.ndarray) -> np.ndarray:
        """
        Calculates the error between the true (y_true)
        and predicted (y_pred) values

        Parameters
        ----------
            y_true: numpy.ndarray
            y_pred: numpy.ndarray

        Returns
        -------
            A ``numpy.ndarray`` of elements having the cost function applied
        """
        pass

    def derivative(y_true: np.ndarray,
                   y_pred: np.ndarray) -> np.ndarray:
        """
        Calculates the derivative of the error between
        the true (y_true) and predicted (y_pred) values

        Parameters
        ----------
            y_true: numpy.ndarray
            y_pred: numpy.ndarray
        Returns
        -------
            A ``numpy.ndarray`` of elements having derivative
            of the cost function applied
        """
        pass


class Activation(Layer):
    """
    Applies a given activation function to the input

    Attributes
    ----------
    input  : numpy.ndarray
        The input matrix to be used by the layer

    output : numpy.ndarray
        The output matrix produced by the layer

    activator            : typing.Callable
        The activation function

    activator_derivative : typing.Callable
        The derivation of the activation function

    Methods
    -------
    forward(input: numpy.ndarray) -> numpy.ndarray:
        Computes the activated value after applying the activation function

    backward(output_gradient: numpy.ndarray,
              learning_rate: float = 0.1) -> numpy.ndarray:
        Computes the derivative of error w.r.t the inputs for this layer
    """

    def __init__(self, activator: typing.Callable,
                 activator_derivative: typing.Callable):
        """
        Constructs all the necessary attributes for the Activation object

        Parameters
        ----------
            activator: typing.Callable
                The function to be used as the activation function

            activator_derivative: typing.Callable
                The function to be used as the derivative of the activation function
        """
        self.activator = activator
        self.activator_derivative = activator_derivative

    def forward(self, input: np.ndarray) -> np.ndarray:
        self.input = input
        return self.activator(self.input)

    def backward(self, output_gradient: np.ndarray,
                 learning_rate: float = 0.1) -> np.ndarray:
        return np.multiply(output_gradient,
                           self.activator_derivative(self.input))
