import typing as th


def accuracy(y, y_hat) -> float:
    # todo: for you to implement
    return sum(y == y_hat) / len(y_hat)


def f1(y, y_hat, alpha: float = 0.5, beta: float = 1.):
    # todo: for you to implement
    return ((1 + beta ** 2) * precision(y, y_hat) * recall(y, y_hat)) / (
                beta ** 2 * precision(y, y_hat) + recall(y, y_hat))
    pass


def precision(y, y_hat) -> float:
    # todo: for you to implement
    y = y[y_hat == 1]
    TP = sum(y == 1)
    FP = sum((1 - y) == 1)
    return TP / (TP + FP)


def recall(y, y_hat) -> float:
    # todo: for you to implement
    y_hat = y_hat[y == 1]
    TP = sum(1 == y_hat)
    FN = sum(1 == (1 - y_hat))
    return TP / (TP + FN)


evaluation_functions = dict(accuracy=accuracy, f1=f1, precision=precision, recall=recall)


def evaluate(y, y_hat) -> th.Dict[str, float]:
    """
    :param y: ground truth
    :param y_hat: model predictions
    :return: a dictionary containing evaluated scores for provided values
    """
    return {name: func(y, y_hat) for name, func in evaluation_functions.items()}
