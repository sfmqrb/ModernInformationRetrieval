import typing as th
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn import svm

# since you can use sklearn (or other libraries) implementations for this task,
#   you can either initialize those implementations in the provided format or use them as you wish


class SVM(BaseEstimator, ClassifierMixin):
    def __init__(self, c):
        self.c = c
        self.kernel = 'linear'
        self.clf = svm.SVC(kernel = self.kernel, C=self.c)

    def fit(self, x, y, **fit_params):
        self.clf = self.clf.fit(x, y)
        return self

    def predict(self, x, y=None):
        self.p = self.clf.predict(x)
        return self.p

    def acc(self, y_val):
        return sum(self.p == y_val) / len(y_val)

    def get_coef(self):
        return self.clf.coef_

    def get_intercept(self):
        return self.clf.intercept_