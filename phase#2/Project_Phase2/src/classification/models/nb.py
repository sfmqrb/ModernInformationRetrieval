import typing as th  # Literals are available for python>=3.8
from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np
import math


class NaiveBayes(BaseEstimator, ClassifierMixin):
    kind = None
    def __init__(self, kind, bc, alpha = 0):
        self.kind = kind
        self.bc = bc
        self.alpha = alpha

    def fit(self, x, y, **fit_params):
        # todo: for you to implement
        if self.kind[0] == 'g':
            self.calc_stat(x, y)
            self.calc_log_prior(y)
        else:
            self.calc_log_prior(y)
            self.calc_mid(x, y)
            self.calc_prob_bern(x, y)
        return self

    def predict(self, x):
        if self.kind[0] == 'g':
            self.p = (x.apply(self.calc_post_g, axis=1)).to_numpy()
        else:
            self.p = (x.apply(self.calc_post_b, axis=1)).to_numpy()
        return self.p

    def calc_post_b(self, vec):
        post0 = self.prior[0]
        post1 = self.prior[1]

        pl0 = self.prob_y0
        pl0_0 = 1 - pl0
        pl1 = self.prob_y1
        pl1_0 = 1 - pl1

        pl0 = np.log(pl0)
        pl0_0 = np.log(pl0_0)
        pl1 = np.log(pl1)
        pl1_0 = np.log(pl1_0)

        vec = vec > self.mid

        post0 += vec.dot(pl0) + (~vec).dot(pl0_0)
        post1 += vec.dot(pl1) + (~vec).dot(pl1_0)

        if post0 <= post1:
            return 1
        return 0

    def calc_post_g(self, vec):
        post0 = self.prior[0]
        post1 = self.prior[1]
        post0 += sum(self.log_pdf(self.mean0, self.std0, vec))
        post1 += sum(self.log_pdf(self.mean1, self.std1, vec))
        if post0 <= post1:
            return 1
        return 0

    def calc_cut(self, X, y):
        X1 = X[y == 1]
        self.cut1 = (X1.apply(self.cut, axis=0)).to_numpy()
        X0 = X[y == 0]
        self.cut0 = (X1.apply(self.cut, axis=0)).to_numpy()

    def calc_stat(self, X, y):
        self.mean1 = (X[y == 1]).mean()
        self.std1 = (X[y == 1]).std()
        self.mean0 = (X[y == 0]).mean()
        self.std0 = (X[y == 0]).std()

    def log_pdf(self, mean, std, vec):
        return np.log(self.g_pdf(mean, std, vec))

    def g_pdf(self, mean, std, vec):
        exp_part = np.exp(-1 / 2 * ((vec - mean) / std) ** 2)
        return (1 / (math.sqrt(2 * math.pi) * std)) * exp_part

    def calc_log_prior(self, y):
        prior_log = np.log(np.array([sum(y == 0) / len(y), sum(y == 1) / len(y)]))
        self.prior = prior_log

    def find_mid(self, Arr):
        mid = None
        if self.bc == "maxminaverage":
            max_ = Arr.max()
            min_ = Arr.min()
            mid = (max_ + min_) / 2
        elif self.bc == 'midpoint':
            mid = np.median(Arr, axis = 0)
        else:
            mid = np.mean(Arr, axis = 0)

        return mid

    def calc_mid(self, X, y):
        self.mid = self.find_mid(X)
        return self.mid

    def calc_prob_bern(self, X, y):
        x1 = X[y == 1]
        x0 = X[y == 0]
        self.prob_y1, self.prob_y0 = (x1 > self.mid).sum() / len(x1), (x0 > self.mid).sum() / len(x0)
        if self.bc == 'smooth':
            alpha = self.alpha
            self.prob_y1 = self.prob_y1 * (1 - alpha) + alpha / 2
            self.prob_y0 = self.prob_y0 * (1 - alpha) + alpha / 2


    def acc(self, val_y):
        n_right_guess = sum(val_y == self.p)
        n = len(val_y)
        return n_right_guess / n