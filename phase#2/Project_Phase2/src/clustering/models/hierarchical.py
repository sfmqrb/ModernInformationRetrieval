import typing as th
from sklearn.base import ClusterMixin, BaseEstimator
# since you can use sklearn (or other libraries) implementations for this task,
#   you can either initialize those implementations in the provided format or use them as you wish
from sklearn.cluster import AgglomerativeClustering


class Hierarchical(ClusterMixin, BaseEstimator):
    def __init__(self, cc, linkage):
        self.cc = cc
        self.linkage = linkage
        self.ac = AgglomerativeClustering(n_clusters=cc, linkage=linkage)
        pass

    def fit(self, x):
        self.p = self.ac.fit_predict(x)
        # todo: for you to implement
        return self

    def predict(self, x):
        return self.p
