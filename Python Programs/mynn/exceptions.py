class UnfittedModelError(Exception):
    """
    UnfittedModelError is an exception which is thrown
    if a Model is trained before fitting

    Attributes
    ----------
        message: str
            An optional message with the Error
    """

    def __init__(self, message: str = ""):
        self.message = message
        super().__init__(message)


class InvalidCostFunctionError(Exception):
    """
    InvalidCostFunctionError is an exception which is thrown
    if a Model is trained with an abnormal cost function object

    Attributes
    ----------
        message: str
            An optional message with the Error
    """

    def __init__(self, message: str = ""):
        self.message = message
        extra = """\nCustom Cost Functions can be created by extending the mynn.base.CostFunction class"""
        super().__init__(message + extra)


class InvalidLearningRateError(Exception):
    """
    InvalidLearningRateError is an exception which is thrown
    if a the learning rate specified isn't a number

    Attributes
    ----------
        message: str = "Learning Rate must be a number"
            An optional message with the Error
            Defaults to "Learning Rate must be a number"
    """

    def __init__(self, message: str = "Learning Rate must be a number"):
        self.message = message
        super().__init__(message)
