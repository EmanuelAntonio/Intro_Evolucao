from implementacao01 import *

def encontrar_palavra(palavra, alfabeto):
    size = len(palavra)
    cont = 1
    rand_palavra = ''.join(random.choice(alfabeto) for _ in range(size))

    while rand_palavra != palavra:
        rand_palavra = ''.join(random.choice(alfabeto) for _ in range(size))
        cont += 1
    return cont


def encontrar_palavra_mutacao(palavra, alfabeto, u):
    size = len(palavra)
    rand_palavra = ''.join(random.choice(alfabeto) for _ in range(size))
    N = 1
    alfabeto_corrigido = {}

    for i in alfabeto:
        alf = copy.deepcopy(alfabeto)
        alf.remove(i)
        alfabeto_corrigido[i] = alf

    while rand_palavra != palavra:
        for i in range(size):
            if np.random.random_sample() <= u:
                str_aux = list(rand_palavra)
                str_aux[i] = random.choice(alfabeto_corrigido[rand_palavra[i]])
                rand_palavra = "".join(str_aux)
        N += 1
    return N


def implementacao03():
    num_randomizacoes = 20
    distribuicao = np.zeros(num_randomizacoes)
    palavra = 'agctttt'
    # palavra = 'agcttttcattctgactgcaacgggcaata'
    alfabeto = ['t', 'g', 'c', 'a']
    for i in range(num_randomizacoes):
        distribuicao[i] = encontrar_palavra(palavra, alfabeto)
    print("Para encontrar\"" + palavra + "\"com o alfabeto", alfabeto, "demorou em média", np.average(distribuicao),
          "tentativas, com desvio padrão", np.std(distribuicao))


def implementacao031():
    num_randomizacoes = 200
    du = 0.001
    us = np.arange(du, 1 + du, du)
    # us = np.array([1.0])
    distribuicao_mut = np.zeros((num_randomizacoes, 2))
    distribuicao = np.zeros(num_randomizacoes)
    distribuicao_u = np.zeros(us.shape[0])
    # palavra = 'tgtacga'
    palavra = 'tgtac'
    alfabeto = ['t', 'g', 'c', 'a']
    cont = 0
    for u in us:
        print(u)
        for i in range(num_randomizacoes):
            N = encontrar_palavra_mutacao(palavra, alfabeto, u)
            distribuicao_mut[i] = N
        distribuicao_u[cont] = np.average(distribuicao_mut[:, 0])
        cont += 1

    for i in range(num_randomizacoes):
        distribuicao[i] = encontrar_palavra(palavra, alfabeto)

    plt.plot(us, distribuicao_u, label="Com Mutação")
    plt.plot(us, np.ones(us.shape[0]) * np.average(distribuicao), label="Sem Mutação")
    # plt.ylim(0, np.max(distribuicao_u))
    plt.xlabel('u')
    plt.ylabel('MED(N)')
    plt.legend(loc='upper right')
    plt.savefig(path + "/implementacao03/grafico.png", dpi=300)
    plt.close()

    plt.plot(us[100:], distribuicao_u[100:], label="Com Mutação")
    plt.plot(us[100:], np.ones(us.shape[0] - 100) * np.average(distribuicao), label="Sem Mutação")
    # plt.ylim(0, np.max(distribuicao_u))
    plt.xlabel('u')
    plt.ylabel('MED(N)')
    plt.legend(loc='upper right')
    plt.savefig(path + "/implementacao03/grafico_0.1_1.0.png", dpi=300)
    plt.close()

    plt.plot(us[:100], distribuicao_u[:100], label="Com Mutação")
    plt.plot(us[:100], np.ones(100) * np.average(distribuicao), label="Sem Mutação")
    # plt.ylim(0, np.max(distribuicao_u))
    plt.xlabel('u')
    plt.ylabel('MED(N)')
    plt.legend(loc='upper right')
    plt.savefig(path + "/implementacao03/grafico_0.0_0.1.png", dpi=300)
    plt.close()

    distribuicao_u.dump(path + "/implementacao03/distribuicao_mut_u.npy")
    distribuicao.dump(path + "/implementacao03/distribuicao_rand.npy")
    us.dump(path + "/implementacao03/us.npy")


def calcula_pontuacao(palavra_objetivo, palavra, alfabeto_indice, u):
    pontuacao = 0
    for i in range(len(palavra)):
        u1 = alfabeto_indice[palavra[i]]
        u0 = alfabeto_indice[palavra_objetivo[i]]
        if u0 == u1:
            pontuacao += u[u1, u0]
        else:
            pontuacao += u[u1, u0]
    return pontuacao


def mutacao(palavra, alfabeto, indice_alfabeto, u):
    palavra_mut = copy.deepcopy(palavra)
    size = len(palavra_mut)
    for i in range(size):
        rnd = np.random.random_sample()
        rnd_sum = 0
        u_i = indice_alfabeto[palavra_mut[i]]
        for j in range(len(alfabeto)):
            rnd_sum += u[u_i, j]
            if rnd_sum >= rnd:
                str_aux = list(palavra_mut)
                str_aux[i] = alfabeto[j]
                palavra_mut = "".join(str_aux)
                break
    return palavra_mut


def carregar_palavra_base_dados(name, tam):
    base_dados = open(path + "/implementacao03/E.coli-sequence.txt")
    palavra = ""
    count = 0
    for linha in base_dados.readlines():
        linha = str.lower(linha)
        for c in linha:
            palavra = palavra + c
            count += 1
            if count == tam:
                return palavra


def implementacao032():
    # u = np.array([[0.7, 0.1, 0.1, 0.1],[0.1, 0.7, 0.1, 0.1], [0.1, 0.1, 0.7, 0.1], [0.1, 0.1, 0.1, 0.7]])
    # u = np.array([[0.6, 0.05, 0.05, 0.3],[0.05, 0.6, 0.3, 0.05], [0.05, 0.3, 0.6, 0.05], [0.3, 0.05, 0.05, 0.6]])
    u = np.array(
        [[0.7, 0.025, 0.025, 0.25], [0.025, 0.7, 0.25, 0.025], [0.025, 0.25, 0.7, 0.025], [0.25, 0.025, 0.025, 0.7]])
    # u = np.array([[0.5, 0.1, 0.1, 0.3],[0.1, 0.5, 0.3, 0.1], [0.1, 0.3, 0.5, 0.1], [0.3, 0.1, 0.1, 0.5]])

    palavra = carregar_palavra_base_dados('E.coli-sequence.txt', 7)
    alfabeto = ['a', 't', 'c', 'g']
    alfabeto_indice = {'a': 0, 't': 1, 'c': 2, 'g': 3}
    cont = 0
    N = 10
    size = len(palavra)
    individuos = []
    pontuacoes = []
    max_pontuacao = 0
    indice_max_pontuacao = -1
    for i in range(N):
        individuos.append(''.join(random.choice(alfabeto) for _ in range(size)))
        pontuacao = calcula_pontuacao(palavra, individuos[i], alfabeto_indice, u)
        pontuacoes.append(pontuacao)
        if pontuacao > max_pontuacao:
            max_pontuacao = pontuacao
            indice_max_pontuacao = i
    objetivo = calcula_pontuacao(palavra, palavra, alfabeto_indice, u)
    # print("Objetivo: ", objetivo)
    # print(max_pontuacao)
    # print(individuos[indice_max_pontuacao])
    cont = 1
    while max_pontuacao < (objetivo - EPSILON):
        melhor_individuo = copy.deepcopy(individuos[indice_max_pontuacao])
        individuos.clear()
        pontuacoes.clear()
        indice_max_pontuacao = -1
        max_pontuacao = 0
        for i in range(N):
            individuo = mutacao(melhor_individuo, alfabeto, alfabeto_indice, u)
            individuos.append(individuo)
            pontuacao = calcula_pontuacao(palavra, individuo, alfabeto_indice, u)
            pontuacoes.append(pontuacao)
            if pontuacao > max_pontuacao:
                max_pontuacao = pontuacao
                indice_max_pontuacao = i
        # print(max_pontuacao)
        # print(individuos[indice_max_pontuacao])
        cont += 1
    return cont