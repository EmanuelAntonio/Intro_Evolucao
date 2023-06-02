from implementacao01 import *


def implementacao06():
    casos = ["padrao", "dominancia", "codominancia", "sobredominancia", "desvantagem"]
    w0 = np.array([[1, 0.5, 0.25, 0], [1, 1, 0.9, 1], [1, 0.9, 0.8, 2], [0.9, 1, 0.9, 3], [1, 0.9, 1, 4]],
                  dtype=np.float64)
    p0 = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], dtype=np.float64)
    t = 150
    AA = np.array(range(t), dtype=np.float64)
    Aa = np.array(range(t), dtype=np.float64)
    aa = np.array(range(t), dtype=np.float64)
    p_array = np.array(range(t), dtype=np.float64)
    q_array = np.array(range(t), dtype=np.float64)
    delta_p = np.array(range(t), dtype=np.float64)
    w_med = np.array(range(t), dtype=np.float64)
    # inicialização das variáveis
    for w in w0:
        for p in p0:
            AA[0] = p * p
            Aa[0] = 2 * p * (1 - p)
            aa[0] = (1 - p) * (1 - p)
            p_array[0] = p
            q_array[0] = 1 - p
            delta_p[0] = 0
            t0 = 1

            while t0 < t:
                w_avg = AA[t0 - 1] * w[0] + Aa[t0 - 1] * w[1] + aa[t0 - 1] * w[2]
                p_array[t0] = (AA[t0 - 1] * w[0] + 0.5 * Aa[t0 - 1] * w[1]) / w_avg
                q_array[t0] = (aa[t0 - 1] * w[0] + 0.5 * Aa[t0 - 1] * w[1]) / w_avg
                AA[t0] = p_array[t0] * p_array[t0]
                Aa[t0] = 2 * p_array[t0] * q_array[t0]
                aa[t0] = q_array[t0] * q_array[t0]
                w_med[t0] = w_avg
                delta_p[t0] = p_array[t0] - p_array[t0 - 1]
                t0 += 1