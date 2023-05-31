import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2
import random
import time
import copy

EPSILON = 1E-6

path = "D:/Evolucao"

def Hardy_Weinberg(p, q):
    return np.multiply(p, p) + 2 * np.multiply(p, q) + np.multiply(q, q)


#https://towardsdatascience.com/chi-square-test-with-python-d8ba98117626
def qui_quadrado(obs, exp):
    # significance level
    alpha = 0.05

    chi_squared = np.sum(((obs - exp)**2) / exp)
    critical_value = chi2.ppf(q=1 - alpha, df=1)
    p_value = 1 - chi2.cdf(x=chi_squared, df=1)
    return [chi_squared, critical_value, p_value]


def mutacao_unidirecional(p0, q0, u, t):
    p = np.zeros(t)
    q = np.zeros(t)
    X = np.zeros((t, 3))
    p[0] = p0
    q[0] = q0
    X[0] = p0
    t0 = 0
    while t0 < t - 1:
        p[t0 + 1] = (1 - u) * p[t0]
        q[t0 + 1] = q[t0] + u * p[t0]
        obs = 100 * np.array([p[t0 + 1]**2, 2 * p[t0 + 1] * q[t0 + 1], q[t0 + 1]**2])
        exp = 100 * np.array([p0**2, 2 * p0 * q0, q0**2])
        X[t0 + 1] = qui_quadrado(obs, exp)
        t0 += 1
    return p, q, X


def implementacao01():
    t = int(10000)
    # u0 = np.array([1E-1, 1E-2, 1E-3, 1E-4, 1E-5, 1E-6, 1E-7, 1E-8, 1E-9, 1E-10])
    u0 = np.array([0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1])
    p0 = np.array([0.1, 0.5, 0.9])
    t0 = np.array(range(t))
    chisquare = open(path + "/implementacao01/chi_square_test.txt", "w")
    pq = open(path + "/implementacao01/pq.txt", "w")

    for u in u0:
        cont = 1
        fig = plt.figure(figsize=(12, 5))
        for P in p0:
            p, q, X = mutacao_unidirecional(P, 1 - P, u, t)

            EHW = 0
            for i in range(X.shape[0]):
                if X[i, 0] <= X[i, 1]:
                  EHW = i

            ax = fig.add_subplot(1, p0.shape[0], cont, xlabel='gerações', ylabel='frequência(p0=' + str(P) + ')',
                                 box_aspect=1)
            ax.plot(t0[:70], p[:70], '-g', label='p')
            ax.plot(t0[:70], q[:70], '-b', label='q')
            ax.vlines(x=EHW, ymin=0, ymax=1, colors='purple', ls=':', lw=2, label='EHW = ' + str(EHW))
            plt.legend(loc='upper right')
            plt.grid()
            chisquare.write("p0 = " + str(P) + " q0 = " + str(1 - P) + " u_" + str(u) + " EHW = " + str(EHW) + "\nchi_squared\tcritical_value\tp_value\n" + str(X) + "\n")
            t_min = 0
            for i in range(1, t):
                if np.abs(p[i] - q[i]) < np.abs(p[t_min] - q[t_min]):
                    t_min = i
            pq.write("p0 = " + str(P) + " q0 = " + str(1 - P) + " 2pq = " + str(2 * p[p.shape[0]-1] * q[p.shape[0]-1]) + " t_conv = " + str(t_min) + "\n")
            cont += 1
        plt.tight_layout()
        plt.suptitle('Frequências Gênicas com Mutação Unidirecional (u=' + str(u) + ')')
        plt.savefig(path + "/implementacao01/u_" + f"{u:e}" + ".png", dpi=300)
        plt.close(fig)

    chisquare.close()
    pq.close()

