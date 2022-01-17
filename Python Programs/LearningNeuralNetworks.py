import numpy as np


class NeuralNetworkPractice:
    def __init__(self, weights=None, bias=None,
                 learning_rate=0.05, num_iters=20000,
                 random_state=118):
        '''
        This method initialises the NN class
        Required Parameters: X and y
        X : is the training data for the model
        '''

        '''
        here we define the hyper parameters for the NN
        this line ensures that the same random numbers are generated
        every time the code is executed
        '''
        np.random.seed(random_state)
        self.learning_rate = learning_rate
        self.num_iters = num_iters

        '''
        here we define random weights at the beginning of the training
        these values are floats between 0 and 1
        similar to the feature and answer sets,
        this is an array
        '''
        if not isinstance(weights, np.ndarray):
            self.weights = np.random.rand(self.X.shape[1], 1)
        else:
            self.weights = weights

        '''
        here we define a random bias at the beginning of the training
        its value is a float between 0 and 1
        this is not an array, it is a number
        '''
        if not isinstance(bias, np.ndarray):
            self.bias = np.random.rand(1)
        else:
            self.bias = bias

    def _sigmoid(self, x):
        '''
        Activation Function for the neural network
        here x can be either a number or an array
        '''
        return 1 / (1 + np.exp(-x))

    def _sigmoid_derivative(self, x):
        '''
        Derivative of the activation function
        here x can be either a number or an array
        '''
        return self._sigmoid(x) * (1 - self._sigmoid(x))
        '''
        this statement can also be given as
        return np.exp(x)/ ((1+np.exp(x)) ** 2)
        which is the derivative obtained
        on differentiation by hand!
        '''

    def train(self, X, y):
        '''
        Used to train the NN by updating the weights
        and bias while iterating num_iters times
        '''
        for i in range(self.num_iters):
            '''
            this line resets the training inputs data back to
            the original feature set every iteration
            '''
            training_inputs = X

            '''
            the first step of the feed forward process
            here we find the dot product of the inputs
            and the weight vector and add bias to it
            '''
            XW = np.dot(X, self.weights) + self.bias

            '''
            the second step of the feed forward process
            here we pass the dot product through the
            sigmoid activation function which returns
            predictions about the given inputs
            '''
            prediction = self._sigmoid(XW)

            '''
            the first step of the backpropagation process
            here we find the errors between our predicted values
            and the actual answers of the feature set
            '''
            error = prediction - y

            '''
            the second step of the backpropagation process
            the cost function for this NN was defined as
            MSE = 1/n ∑ (predicted - observed)² for all inputs
            we find the derivative of this function for all weights
            to find the function minima in order to optimize our
            weights and bias for the NN model
            we use the chain rule of differentiation to do this
            dcost_dpred is the derivative of the cost function with respect to the predictions
            dpred_dp is the derivative of the predicted values with the input dot product
            NOTE : in the differentiantion, we also get a dp/dweights
            but since dp = x₁w₁ + x₂x₂ .... + b
            dp/dweight is actually equal to the input vector itself
            '''
            dcost_dpred = error
            dpred_dp = self._sigmoid_derivative(prediction)

            # slope = training_inputs * dcost_dpred * dpred_dp

            prediction_delta = dcost_dpred * dpred_dp
            training_inputs = X.T

            # update the weights for the next iteration
            self.weights -= self.learning_rate * np.dot(training_inputs, prediction_delta)

            # update the bias for the next iteration
            for val in prediction_delta:
                self.bias -= self.learning_rate * val

    def predict(self, X_test):
        return 1 if self._sigmoid(np.dot(X_test, self.weights) + self.bias) > 0.5 else 0

    def predict_proba(self, X_test):
        return self._sigmoid(np.dot(X_test, self.weights) + self.bias)[0][0]


if __name__ == '__main__':
    '''
    The training data for the NN
    the first line is the values of
    the 3 features we give to the NN
    to test for lung cancer
    which are , in that order
    smokers, obese, exercise, age > 25
    '''
    feature_set = np.array([[0, 1, 0, 1],   # not a smoker, obese, no exercise, older than 30
                            [0, 0, 1, 0],   # not a smoker, not obese, exercises, younger than 30
                            [1, 0, 1, 1],   # is a smoker, not obese, no exercise, older than 30
                            [1, 0, 1, 0],   # is a smoker, not obese, exercises, younger than 30
                            [1, 1, 0, 1]])  # is a smoker, obese, no exercise, older than 30

    '''
    the next line is array of  the known answers for the above feature set
    1 means diabetic, 0 means not diabetic
    '''
    answers = np.array([[0, 0, 1, 0, 1]])

    # this lines just reshapes the array to contain multiple rows instead of columns
    answers = answers.reshape(feature_set.shape[0], 1)

    np.random.seed(5)

    '''
    here we define random weights at the beginning of the training
    these values are floats between 0 and 1
    similar to the feature and answer sets,
    this is an array
    '''
    weights = np.random.rand(feature_set.shape[1], 1)

    '''
    here we define a random bias at the beginning of the training
    its value is a float between 0 and 1
    this is not an array, it is a number
    '''
    bias = np.random.rand(1)
    learning_rate = 0.025

    model = NeuralNetworkPractice(weights, bias, learning_rate)
    model.train(feature_set, answers)
    X_test = np.array([[0, 0, 1, 1]])  # not a smoker, not obese, exercises, older than 30
    has_cancer = model.predict(X_test)
    proba = round(model.predict_proba(X_test) * 100, 2)
    if proba > 75:
        print('Has lung cancer!')
    elif proba < 25:
        print("Doesn't have lung cancer!")
    else:
        if proba > 50:
            print('May have lung cancer!')
        else:
            print('May not have lung cancer!')
        print(f'Probability of having lung cancer is: {proba} %')
