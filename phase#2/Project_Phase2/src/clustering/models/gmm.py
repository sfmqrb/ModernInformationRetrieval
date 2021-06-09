import typing as th
from abc import ABCMeta
from sklearn.base import DensityMixin, BaseEstimator

# since you can use sklearn (or other libraries) implementations for this task,
#   you can either initialize those implementations in the provided format or use them as you wish
from sklearn.mixture import GaussianMixture


class GMM(DensityMixin, BaseEstimator, metaclass=ABCMeta):
    def __init__(self, cc, mi):
        self.cc = cc
        self.mi = mi
        self.gmm = GaussianMixture(n_components=cc, max_iter=mi)
        # todo: initialize parameters
        pass

    def fit(self, x):
        self.gmm = self.gmm.fit(x)
        # todo: for you to implement
        return self

    def predict(self, x):
        self.p = self.gmm.predict(x)
        # todo: for you to implement
        return self.p
