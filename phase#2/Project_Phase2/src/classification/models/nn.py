import typing as th
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.neural_network import MLPClassifier

# since you can use sklearn (or other libraries) implementations for this task,
#   you can either initialize those implementations in the provided format or use them as you wish


class NeuralNetwork(BaseEstimator, ClassifierMixin):
    def __init__(self, act, solver, lr, hls):
        self.clf = MLPClassifier(solver=solver, learning_rate=lr, activation=act,
                            hidden_layer_sizes=hls, max_iter=1_000_000_000)
        pass

    def fit(self, x, y, **fit_params):
        self.clf = self.clf.fit(x, y)
        return self

    def predict(self, x):
        self.p = self.clf.predict(x)
        return self.p

    def acc(self, y_val):
        return sum(self.p == y_val) / len(y_val)
