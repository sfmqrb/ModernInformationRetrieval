import typing as th
from sklearn.base import TransformerMixin, ClusterMixin, BaseEstimator
import numpy as np
import pandas as pd

class KMeans(TransformerMixin, ClusterMixin, BaseEstimator):
    def __init__(self, cc: int, mi: int):
        self.centroids = None
        self.cc = cc
        self.mi = mi

    def fit(self, x):
        # todo: for you to implement
        self.centroids = x.sample(self.cc, )
        self.centroids = self.centroids.to_numpy()
        self.labels = np.zeros((len(x), 1), dtype=np.int8)

        for i in range(self.mi):
            for idx, row in x.iterrows():
                row = np.array(row)
                sub = self.centroids - row
                power_2 = np.power(sub, 2)
                dist = np.sum(power_2, axis=1)
                self.labels[idx] = np.argmin(dist)

            self.centroids[:, :] = 0
            self.numberOfEachLabel = np.zeros((self.cc, 1))

            for i in range(len(x)):
                label = self.labels[i]
                self.centroids[label, :] += np.array(x.iloc[i, :])
                self.numberOfEachLabel[label] += 1

            self.centroids = self.centroids / self.numberOfEachLabel

        return self

    def predict(self, x):

        self.p = np.zeros((len(x)))

        for idx, row in x.iterrows():
            row = np.array(row)
            sub = np.subtract(self.centroids, row)
            power_2 = np.power(sub, 2)
            dist = np.sum(power_2, axis=1)
            self.p[idx] = np.argmin(dist)

        return self.p