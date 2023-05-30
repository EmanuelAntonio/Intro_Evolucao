from implementacao01 import *


def plot_p_t(p, t, caso):
    plt.plot(t, p, label="p")
    plt.plot(t, np.ones_like(p) - p, label="q")
    plt.title("p x t (p0 = " + str(p[0]) + ")")
    plt.legend()
    plt.xlabel("t")
    plt.ylabel("p")
    plt.ylim(0, 1)
    plt.savefig(path + "/implementacao04/" + caso + "_p0_" + str(p[0]) + "_p_x_t.png", dpi=300)
    plt.close()


def plot_p_deltap(p, dp, caso):
    plt.plot(p[1:], dp[1:])
    plt.title("p x Δp (p0 = " + str(p[0]) + ")")
    plt.xlabel("p")
    plt.ylabel("Δp")
    plt.xlim(np.min(p), np.max(p))
    plt.savefig(path + "/implementacao04/" + caso + "_p0_" + str(p[0]) + "_p_x_deltap.png", dpi=300)
    plt.close()


def plot_p_alelo(p, AA, Aa, aa, caso):
    plt.plot(p, AA, label="AA")
    # plt.plot(p, Aa, label="Aa")
    # plt.plot(p, aa, label="aa")
    plt.title("p x AA, Aa, aa (p0 = " + str(p[0]) + ")")
    plt.xlabel("p")
    plt.ylabel("Fequência Alélica")
    plt.legend()
    # plt.savefig(path + "/implementacao04/" + caso + "_p0_" + str(p[0]) + "_p_x_frequencia.png", dpi=300)
    plt.show()
    plt.close()


def plot_p_wmed(p, w_med, caso):
    plt.plot(p[1:], w_med[1:])
    plt.title("p x W_med (p0 = " + str(p[0]) + ")")
    plt.xlabel("p")
    plt.ylabel("w_med")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.savefig(path + "/implementacao04/" + caso + "_p0_" + str(p[0]) + "_p_x_wmed.png", dpi=300)
    plt.close()


def implementacao04():
    # casos = ["padrao", "dominancia", "codominancia", "sobredominancia", "desvantagem"]
    casos = ["desvantagem"]
    # w0 = np.array([[1, 0.5, 0.25, 0], [1, 1, 0.9, 1], [1, 0.9, 0.8, 2], [0.9, 1, 0.9, 3], [1, 0.9, 1, 4]], dtype=np.float64)
    w0 = np.array([[1, 0.5038, 0.2538, 0]], dtype=np.float64)
    # p0 = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], dtype=np.float64)
    p0 = np.array([0.5], dtype=np.float64)
    t = 9
    AA = np.array(range(t), dtype=np.float64)
    Aa = np.array(range(t), dtype=np.float64)
    aa = np.array(range(t), dtype=np.float64)
    p_array = np.array(range(t), dtype=np.float64)
    delta_p = np.array(range(t), dtype=np.float64)
    w_med = np.array(range(t), dtype=np.float64)
    w_array = np.zeros((t, 3))
    # inicialização das variáveis
    for w in w0:
        for p in p0:
            AA[0] = p * p
            Aa[0] = 2 * p * (1 - p)
            aa[0] = (1 - p) ** 2
            p_array[0] = p
            delta_p[0] = 0
            w_array[0, 0] = w[0]
            w_array[0, 1] = w[1]
            w_array[0, 2] = w[2]

            # print("PHW", AA[0] + Aa[0] + aa[0])
            t0 = 1
            while t0 < t:
                w_med[t0] = AA[t0 - 1] * w_array[t0 - 1, 0] + Aa[t0 - 1] * w_array[t0 - 1, 1] + aa[t0 - 1] * w_array[
                    t0 - 1, 2]
                w_array[t0, 0] = w_array[t0 - 1, 0] / w_med[t0]
                w_array[t0, 1] = w_array[t0 - 1, 1] / w_med[t0]
                w_array[t0, 2] = w_array[t0 - 1, 2] / w_med[t0]
                AA[t0] = w_array[t0, 0] * AA[t0 - 1]
                Aa[t0] = w_array[t0, 1] * Aa[t0 - 1]
                aa[t0] = w_array[t0, 2] * aa[t0 - 1]
                p_array[t0] = AA[t0] ** 0.5
                delta_p[t0] = p_array[t0] - p_array[t0 - 1]
                # print("PHW", AA[t0] + Aa[t0] + aa[t0])
                t0 += 1
            # plot_p_t(p_array, range(t), casos[int(w[3])])
            # plot_p_deltap(p_array, delta_p, casos[int(w[3])])
            # plot_p_alelo(p_array, AA, Aa, aa, casos[int(w[3])])
            # plot_p_wmed(p_array, w_med, casos[int(w[3])])
    for q in w_array:
        print('{:f}'.format(q[2]))

