import typing as th
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
import pandas as pd

class KNN(BaseEstimator, ClassifierMixin):
    def __init__(self, k, dist_type):
        # todo: initialize parameters
        self.k = k
        # self.power_dist = power_dist
        self.dist_type = dist_type

    def fit(self, x, y, **fit_params):
        # todo: for you to implement
        self.x_train = x
        self.y_train = y
        return self

    def predict(self, x):
        self.p = self.k_nearest(x)
        return self.p

    def k_nearest_to_vec(self, vec):

        if self.dist_type == "line_1":
            sub = np.subtract(self.x_train, vec)
            sub = np.abs(sub)
            sm = sub.sum(axis=1)

        if self.dist_type == "line_2":
            sub = np.subtract(self.x_train, vec)
            sub = np.abs(sub)
            pw = np.power(sub, 2)
            sm = pw.sum(axis=1)

        elif self.dist_type == 'dot product':
            sub = np.dot(self.x_train, vec)
            sub = sub / (np.linalg.norm(self.x_train, axis= 1))
            sm = -sub + 1
            sm = pd.Series(sm)

        index = sm.nsmallest(self.k).index
        y_vals = self.y_train[index]

        score = self.k / 2 - sum(y_vals)
        if score > 0:
            return 0
        return 1

    def k_nearest(self, x):
        return x.apply(self.k_nearest_to_vec, axis=1)

    def acc(self, val_y):
        n_right_guess = sum(val_y == self.p)
        n = len(val_y)
        return n_right_guess / n