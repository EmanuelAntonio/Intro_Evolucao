from implementacao01 import *


def plot_deltap_t(t, dp, p0, caso, grafico):
    plt.plot(range(1, t - 1, 1), dp[1:-1])
    plt.title("Δp x t " + grafico + "(p0 = " + str(p0) + ")")
    plt.xlabel("t")
    plt.ylabel("Δp")
    plt.savefig(path + "/implementacao06/" + grafico + "_" + caso + "_p0_" + str(p0) + "_p_x_deltap.png", dpi=300)
    plt.close()

def plot_p_t(t, p, q, p0, caso, grafico):
    plt.plot(range(t), p)
    plt.plot(range(t), q)
    plt.title("Frequência Gênica (p0 = " + str(p0) + ")")
    plt.xlabel("t")
    plt.ylabel("Frequência Gênica")
    plt.savefig(path + "/implementacao06/" + grafico + "_" + caso + "_p0_" + str(p0) + "_p_t.png", dpi=300)
    plt.close()


def plot_wmed_t(t, w_med, p0, u, v, caso, grafico):
    plt.plot(range(t), w_med)
    plt.title("W_avg (p0 = " + str(p0) + ", u=" + str(u) + " v=" + str(v) + ")")
    plt.xlabel("t")
    plt.ylabel("Valor adaptativo médio")
    plt.savefig(path + "/implementacao06/" + grafico + "_" + caso + "_p0_" + str(p0) + "_p_t.png", dpi=300)
    plt.close()


def plot_AA_Aa_aa_t(t, AA, Aa, aa, p0, u, v, caso, grafico):
    plt.plot(range(t), AA, label="AA")
    plt.plot(range(t), Aa, label="Aa")
    plt.plot(range(t), aa, label="aa")
    plt.title("Frequência gênica (p0 = " + str(p0) + ", u=" + str(u) + " v=" + str(v) + ")")
    plt.xlabel("t")
    plt.ylabel("Frequência gênica")
    plt.legend()
    plt.savefig(path + "/implementacao06/" + grafico + "_" + caso + "_p0_" + str(p0) + "_p_t.png", dpi=300)
    plt.close()

def implementacao06():
    casos = ["padrao", "dominancia", "codominancia", "sobredominancia", "desvantagem"]
    # w0 = np.array([[1, 0.5, 0.25, 0]], dtype=np.float64)
    w0 = np.array([[1, 0.5, 0.25, 0], [1, 1, 0.9, 1], [1, 0.9, 0.8, 2], [0.9, 1, 0.9, 3], [1, 0.9, 1, 4]], dtype=np.float64)
    # p0 = np.array([0.5], dtype=np.float64)
    p0 = np.array([0.2, 0.5, 0.8], dtype=np.float64)
    t = 40
    AA = np.array(range(t), dtype=np.float64)
    Aa = np.array(range(t), dtype=np.float64)
    aa = np.array(range(t), dtype=np.float64)
    p_array = np.array(range(t), dtype=np.float64)
    q_array = np.array(range(t), dtype=np.float64)
    delta_p = np.array(range(t), dtype=np.float64)
    w_med = np.array(range(t), dtype=np.float64)
    delta_p_deriva = np.array(range(t), dtype=np.float64)
    delta_p_mutacao = np.array(range(t), dtype=np.float64)
    # N0 = np.array([5, 50, 100, 200, 1000])
    N0 = np.array([200])
    prob_deriva = 0.1
    u = 0.06
    v = 0.01
    # inicialização das variáveis
    for N in N0:
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
                    ##############################DERIVA##############################

                    AA_t0 = int(N * p_array[t0 - 1] * p_array[t0 - 1])
                    Aa_t0 = int(N * 2 * p_array[t0 - 1] * (1 - p_array[t0 - 1]))
                    aa_t0 = int(N * (1 - p_array[t0 - 1]) * (1 - p_array[t0 - 1]))
                    mortes_AA = 0
                    for _ in range(int(AA_t0)):
                        prob_morte = np.random.random_sample()
                        if prob_morte < prob_deriva:
                            mortes_AA += 1
                    AA_t0 -= mortes_AA
                    mortes_Aa = 0
                    for _ in range(int(Aa_t0)):
                        prob_morte = np.random.random_sample()
                        if prob_morte < prob_deriva:
                            mortes_Aa += 1
                    Aa_t0 -= mortes_Aa
                    mortes_aa = 0
                    for _ in range(int(aa_t0)):
                        prob_morte = np.random.random_sample()
                        if prob_morte < prob_deriva:
                            mortes_aa += 1
                    aa_t0 -= mortes_aa
                    p_array[t0] = (2 * AA_t0 + Aa_t0) / (2 * AA_t0 + 2 * Aa_t0 + 2 * aa_t0)
                    q_array[t0] = 1 - p_array[t0]
                    delta_p_deriva[t0] = p_array[t0] - p_array[t0 - 1]

                    ########################MUTACAO_BIDIRECIONAL########################

                    p_aux = p_array[t0]
                    q_aux = q_array[t0]
                    p_array[t0] = (1 - u) * p_aux + v * q_aux
                    q_array[t0] = (1 - v) * q_aux + u * p_aux
                    delta_p_mutacao[t0] = p_array[t0] - p_aux

                    ##########################SELECAO_NATURAL##########################

                    AA_aux = p_array[t0] * p_array[t0]
                    Aa_aux = 2 * p_array[t0] * q_array[t0]
                    aa_aux = q_array[t0] * q_array[t0]
                    w_avg = AA_aux * w[0] + Aa_aux * w[1] + aa_aux * w[2]
                    p_array[t0] = (AA_aux * w[0] + 0.5 * Aa_aux * w[1]) / w_avg
                    q_array[t0] = (aa_aux * w[2] + 0.5 * Aa_aux * w[1]) / w_avg
                    AA[t0] = p_array[t0] * p_array[t0]
                    Aa[t0] = 2 * p_array[t0] * q_array[t0]
                    aa[t0] = q_array[t0] * q_array[t0]
                    w_med[t0] = w_avg
                    delta_p[t0] = p_array[t0] - AA_aux ** 0.5

                    ###################################################################

                    t0 += 1

                plot_deltap_t(t, delta_p_deriva, p, casos[int(w[3])], "Δp_deriva_N_" + str(N))
                plot_deltap_t(t, delta_p_mutacao, p, casos[int(w[3])], "Δp_mutacao_N_" + str(N))
                plot_deltap_t(t, delta_p, p, casos[int(w[3])], "Δp_selecao_N_" + str(N))
                plot_p_t(t, p_array, q_array, p, casos[int(w[3])], "frequencia_geracao_N_" + str(N))
                plot_wmed_t(t, w_med, p, u, v, casos[int(w[3])], "w_med_N_" + str(N))
                plot_AA_Aa_aa_t(t, AA, Aa, aa, p, u, v, casos[int(w[3])], "AA_Aa_aa_N_" + str(N))
