from implementacao01 import *


def plot_p_t(t, p_array, N_locus, marcadores):
    for i in range(N_locus):
        plt.scatter(range(t), p_array[i, :], label="Loco " + str(i), marker=marcadores[i])

    plt.xlabel("t")
    plt.ylabel("p")
    plt.ylim(0, 1)
    plt.gca().set_aspect(50)
    plt.legend()
    plt.show()


def implementacao05():
    marcadores = [".", "P", "*", "+", "x", "d", "X"]
    N_locus = 7
    t = 100
    N_p = np.zeros(N_locus)
    prob_deriva = 0.6
    p0 = 0.5
    p_array = np.zeros((N_locus, t))
    for i in range(N_locus):
        # N_p[i] = random.choice(range(5, 200, 1))
        N_p[i] = 100
        p_array[i, 0] = p0
    t0 = 0
    while t0 < t - 1:
        print("t0 ", t0)
        N_l = 0
        while N_l < N_locus:
            N = N_p[N_l]
            AA = int(N * p_array[N_l, t0] * p_array[N_l, t0])
            Aa = int(N * 2 * p_array[N_l, t0] * (1 - p_array[N_l, t0]))
            aa = int(N * (1 - p_array[N_l, t0]) * (1 - p_array[N_l, t0]))
            mortes_AA = 0
            print(AA, Aa, aa)
            for _ in range(int(AA)):
                prob_morte = np.random.random_sample()
                if prob_morte < prob_deriva:
                    mortes_AA += 1
            AA -= mortes_AA
            mortes_Aa = 0
            for _ in range(int(Aa)):
                prob_morte = np.random.random_sample()
                if prob_morte < prob_deriva:
                    mortes_Aa += 1
            Aa -= mortes_Aa
            mortes_aa = 0
            for _ in range(int(aa)):
                prob_morte = np.random.random_sample()
                if prob_morte < prob_deriva:
                    mortes_aa += 1
            aa -= mortes_aa
            p_array[N_l, t0 + 1] = (2 * AA + Aa) / (2 * AA + 2 * Aa + 2 * aa)
            print("p ", p_array[N_l, t0 + 1])
            N_l += 1
        t0 += 1
    plot_p_t(t, p_array, N_locus, marcadores)
