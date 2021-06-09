import typing as th
import pandas as pd
import numpy as np
from sklearn.metrics.cluster import adjusted_rand_score

def purity(y, y_hat) -> float:
    class_ls = list(set(y))
    class_ls = [int(x) for x in class_ls]

    cluster_ls = list(set(y_hat))
    cluster_ls = [int(x) for x in cluster_ls]

    purity_data = np.zeros((len(cluster_ls), len(class_ls)))
    purity_df = pd.DataFrame(index=cluster_ls, columns=class_ls, data=purity_data)

    for i in range(len(y)):
        try:
            purity_df.loc[int(y_hat[i]), int(y[i])] += 1
        except Exception as e:
            print(i)
            print(y[i])
            print(y_hat[i])
            print(purity_df)


    n = len(y)
    sum_max_row = purity_df.max(axis=1).sum()
    return sum_max_row / n


def adjusted_rand_index(y, y_hat) -> float:
    return adjusted_rand_score(y, y_hat)


evaluation_functions = dict(purity=purity, adjusted_rand_index=adjusted_rand_index)


def evaluate(y, y_hat) -> th.Dict[str, float]:
    """
    :param y: ground truth
    :param y_hat: model predictions
    :return: a dictionary containing evaluated scores for provided values
    """
    return {name: func(y, y_hat) for name, func in evaluation_functions.items()}
