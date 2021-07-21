import pandas as pd
import numpy as np
import random

def get_train_test(df):
    M = df.to_numpy()
    M_test = np.zeros(M.shape)
    M_train = M.copy()
    for i in range(len(M)):
        for j in range(len(M[0])):
            if M[i][j] > 0:
                if random.random() < 0.2:
                    M_test[i ,j] = M[i, j]                
                    M_train[i, j] = 0
    return M_train, M_test

def get_objective_function(M, P, Q):
    M_hat = P @ Q
    E = M - M_hat
    return np.power(E.flatten()[M.flatten() > 0], 2).sum()


def matrix_factorization(R, P, Q, K, steps=200, alpha=0.0002, beta=0):
    e = get_objective_function(R, P, Q)
    for step in range(steps):
        for i in range(R.shape[0]):
            ei = sum(R[i, :][R[i,:] > 0] - np.dot(P[i,:],Q)[R[i,:] > 0])
            for k in range(K):
                P[i, k] = P[i, k]*(1 - alpha * 2 * -ei) 

        for j in range(R.shape[1]):
            ej = sum(R[:,j][R[:, j] > 0] - np.dot(P,Q[:,j])[R[:, j] > 0])

            for k in range(K):
                Q[k, j] = Q[k, j]*(1 - alpha * 2 * -ej)
        
        e_n = get_objective_function(R, P, Q)
        
    return P, Q


def get_err_test():
    df = pd.read_csv('data.csv')
    df = df.fillna(0)
    M_train, M_test = get_train_test(df)
    P, s, Q = np.linalg.svd(M_train, full_matrices=False)
    s_sqrt = s ** 0.5
    P = P[:, :2]@np.diag(s_sqrt)[:2,:2]
    Q = np.diag(s_sqrt)[:2,:2]@Q[:2, :]
    nP, nQ = matrix_factorization(M_train, P, Q, 2)
    M_new = nP@nQ
    return np.power((M_new - M_test).flatten(), 2)[M_test.flatten() > 0].sum()

