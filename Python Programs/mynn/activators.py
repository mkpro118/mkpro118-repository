from .base import Layer
from .activation import Activation
import numpy as np


class TanH(Activation):
    """
    Uses the Hyperbolic Tangent function as
    the function used by the Activation Layer

    Attributes
    ----------
        None

    Methods
    -------
        None
    """

    def __init__(self):
        def tanh(x: np.ndarray) -> np.ndarray:
            return np.tanh(x)

        def tanh_derivative(x: np.ndarray) -> np.ndarray:
            return 1. - np.tanh(x) ** 2.

        super().__init__(tanh, tanh_derivative)


class Sigmoid(Activation):
    """
    Uses the Sigmoid function as
    the function used by the Activation Layer

    Sigmoid function is defined as below:
                      1
    f(x) =   --------------------
              1  +  (e ** (-x))

    The derivative of the sigmoid is:
    f'(x) = f(x) * (1-f(x))

    Attributes
    ----------
        None

    Methods
    -------
        None
    """

    def __init__(self):
        def sigmoid(x: np.ndarray) -> np.ndarray:
            return 1. / (1. + np.exp(-x))

        def sigmoid_derivative(x: np.ndarray) -> np.ndarray:
            return sigmoid(x) * (1. - sigmoid(x))
        super().__init__(sigmoid, sigmoid_derivative)


class RelU(Activation):
    """
    Uses the RelU function as
    the function used by the Activation Layer

    RelU function is defined as below:
    f(x) = x for x >  0
           0 for x <= 0

    The derivative of the RelU is:
    f'(x) = 1 for x >  0
            0 for x <= 0

    Attributes
    ----------
        None

    Methods
    -------
        None
    """

    def __init__(self, arg):
        def relu(x: np.ndarray) -> np.ndarray:
            return np.maximum(0., x)

        def relu_derivative(x: np.ndarray) -> np.ndarray:
            x[x <= 0.] = 0.
            x[x > 1.] = 1.
            return x

        super().__init__(relu, relu_derivative)


class Softmax(Layer):
    """
    Uses the Softmax function as the activation
    function

    Softmax function is defined as below:
                 e ** (x_i)
    f(x) =   ----------------
              sum(e ** (x_i))

    The derivative of the Softmax is:
    f'(x) = f(x) * (1-f(x))

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
             learning_rate: float = 0.01) -> numpy.ndarray:
        Passes the output to the previous layer in backward propagation
    """

    def forward(self, input: np.ndarray) -> np.ndarray:
        """
        Applies the softmax function on the input matrix

        Parameters
        ----------
        input: numpy.ndarray
            The input matrix to apply the softmax on

        Returns
        -------
            A ``numpy.ndarray`` of the activated result of the softmax function
        """
        tmp = np.exp(input)
        self.output = tmp / np.sum(tmp)
        return self.output

    def backward(self, output_gradient: np.ndarray,
                 learning_rate: float = 0.01) -> np.ndarray:
        """

        Parameters
        ----------
        output_gradient: np.ndarray
            The gradient from the next layer used to
            calculate error in this layer

        learning_rate: float = 0.01
            Determines how the model implements gradient descent
            Default to 0.01

        Returns
        -------
        A ``numpy.ndarray`` of the derivative of the error w.r.t this layer's input
        """
        size = np.size(self.output)
        first = (np.identity(size) - self.output.T) * self.output
        return first @ output_gradient
