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


def implementacao3():
    num_randomizacoes = 2000
    distribuicao = np.zeros(num_randomizacoes)
    palavra = 'agctttt'
    # palavra = 'agcttttcattctgactgcaacgggcaata'
    alfabeto = ['t', 'g', 'c', 'a']
    for i in range(num_randomizacoes):
        distribuicao[i] = encontrar_palavra(palavra, alfabeto)
    print("Implementação 03:\nPara encontrar \"" + palavra + "\" com o alfabeto", alfabeto, "demorou em média", np.average(distribuicao),
          "tentativas, com desvio padrão", np.std(distribuicao))


def implementacao31():
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
    base_dados = open(path + "/" + name)
    palavra = ""
    count = 0
    for linha in base_dados.readlines():
        linha = str.lower(linha)
        for c in linha:
            palavra = palavra + c
            count += 1
            if count == tam:
                return palavra


def implementacao32_cont(palavra, alfabeto, alfabeto_indice, u, N):

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
        cont += 1
    return cont


def implementacao32():
    # u = np.array([[0.7, 0.1, 0.1, 0.1],[0.1, 0.7, 0.1, 0.1], [0.1, 0.1, 0.7, 0.1], [0.1, 0.1, 0.1, 0.7]])
    # u = np.array([[0.6, 0.05, 0.05, 0.3],[0.05, 0.6, 0.3, 0.05], [0.05, 0.3, 0.6, 0.05], [0.3, 0.05, 0.05, 0.6]])
    u = np.array(
        [[0.7, 0.025, 0.025, 0.25], [0.025, 0.7, 0.25, 0.025], [0.025, 0.25, 0.7, 0.025], [0.25, 0.025, 0.025, 0.7]])
    # u = np.array([[0.5, 0.1, 0.1, 0.3],[0.1, 0.5, 0.3, 0.1], [0.1, 0.3, 0.5, 0.1], [0.3, 0.1, 0.1, 0.5]])

    palavra = carregar_palavra_base_dados('E.coli-sequence.txt', 7)
    alfabeto = ['a', 't', 'c', 'g']
    alfabeto_indice = {'a': 0, 't': 1, 'c': 2, 'g': 3}
    N = 100

    distribuicao = []
    for _ in range(20):
        distribuicao.append(implementacao32_cont(palavra, alfabeto, alfabeto_indice, u, N))

    print("Implementação 3.2:\nPara encontrar \"" + palavra + "\" com o alfabeto", alfabeto, "demorou em média", np.average(distribuicao),
          "tentativas, com desvio padrão", np.std(distribuicao))


def melhor_pontuacao(individuos, pontuacoes):
    indice_max = 0
    for i in range(1, len(pontuacoes)):
        if pontuacoes[i] > pontuacoes[indice_max]:
            indice_max = i
    individuo1 = copy.deepcopy(individuos[indice_max])
    del pontuacoes[indice_max]
    del individuos[indice_max]
    indice_max = 0
    for i in range(1, len(pontuacoes)):
        if pontuacoes[i] > pontuacoes[indice_max]:
            indice_max = i
    individuo2 = copy.deepcopy(individuos[indice_max])
    del pontuacoes[indice_max]
    del individuos[indice_max]

    return individuo1, individuo2


def recombinacao(individuo1, individuo2):
    size = len(individuo1)
    rnd = (size - 2) * np.random.random_sample()
    rnd = int(np.round(rnd + 1))
    novo_individuo1 = individuo1[0:rnd] + individuo2[rnd:size]
    novo_individuo2 = individuo2[0:rnd] + individuo1[rnd:size]
    return novo_individuo1, novo_individuo2


def implementacao33_cont(palavra, alfabeto, alfabeto_indice, u, N):
    size = len(palavra)
    individuos = []
    pontuacoes = []
    EPSILON = 1E-3
    for i in range(N):
        individuos.append(''.join(random.choice(alfabeto) for _ in range(size)))
        pontuacao = calcula_pontuacao(palavra, individuos[i], alfabeto_indice, u)
        pontuacoes.append(pontuacao)
    objetivo = calcula_pontuacao(palavra, palavra, alfabeto_indice, u)
    max_pontuacao = np.max(pontuacoes)
    melhor_individuo1, melhor_individuo2 = melhor_pontuacao(individuos, pontuacoes)
    cont = 1
    while max_pontuacao < (objetivo - EPSILON):
        individuos.clear()
        pontuacoes.clear()
        for i in range(0, N, 2):
            novo_individuo1, novo_individuo2 = recombinacao(melhor_individuo1, melhor_individuo2)
            novo_individuo1 = mutacao(novo_individuo1, alfabeto, alfabeto_indice, u)
            novo_individuo2 = mutacao(novo_individuo2, alfabeto, alfabeto_indice, u)
            individuos.append(novo_individuo1)
            individuos.append(novo_individuo2)
            pontuacoes.append(calcula_pontuacao(palavra, novo_individuo1, alfabeto_indice, u))
            pontuacoes.append(calcula_pontuacao(palavra, novo_individuo2, alfabeto_indice, u))
        max_pontuacao = np.max(pontuacoes)
        melhor_individuo1, melhor_individuo2 = melhor_pontuacao(individuos, pontuacoes)
        # print(melhor_individuo1, melhor_individuo2)
        # print(max_pontuacao, objetivo)
        # print(calcula_pontuacao(palavra, melhor_individuo1, alfabeto_indice, u), calcula_pontuacao(palavra, melhor_individuo2, alfabeto_indice, u))
        # print(pontuacoes)
        cont += 1
    return cont


def implementacao33():
    # u = np.array([[0.7, 0.1, 0.1, 0.1],[0.1, 0.7, 0.1, 0.1], [0.1, 0.1, 0.7, 0.1], [0.1, 0.1, 0.1, 0.7]])
    # u = np.array([[0.6, 0.05, 0.05, 0.3],[0.05, 0.6, 0.3, 0.05], [0.05, 0.3, 0.6, 0.05], [0.3, 0.05, 0.05, 0.6]])
    u = np.array([[0.7, 0.025, 0.025, 0.25], [0.025, 0.7, 0.25, 0.025], [0.025, 0.25, 0.7, 0.025], [0.25, 0.025, 0.025, 0.7]])
    # u = np.array([[0.5, 0.1, 0.1, 0.3],[0.1, 0.5, 0.3, 0.1], [0.1, 0.3, 0.5, 0.1], [0.3, 0.1, 0.1, 0.5]])

    palavra = carregar_palavra_base_dados('E.coli-sequence.txt', 7)
    alfabeto = ['a', 't', 'c', 'g']
    alfabeto_indice = {'a': 0, 't': 1, 'c': 2, 'g': 3}
    N = 10

    distribuicao = []
    for _ in range(20):
        distribuicao.append(implementacao33_cont(palavra, alfabeto, alfabeto_indice, u, N))

    print("Implementação 3.3:\nPara encontrar \"" + palavra + "\" com o alfabeto", alfabeto, "demorou em média",
          np.average(distribuicao),
          "tentativas, com desvio padrão", np.std(distribuicao))


def melhor_pontuacao_deriva(individuos, pontuacoes, prob_deriva):
    indice_max = 0
    for i in range(1, len(pontuacoes)):
        rnd = np.random.random_sample()
        if rnd > prob_deriva:
            if pontuacoes[i] > pontuacoes[indice_max]:
                indice_max = i
    individuo1 = copy.deepcopy(individuos[indice_max])
    del pontuacoes[indice_max]
    del individuos[indice_max]
    indice_max = 0
    for i in range(1, len(pontuacoes)):
        rnd = np.random.random_sample()
        if rnd > prob_deriva:
            if pontuacoes[i] > pontuacoes[indice_max]:
                indice_max = i
    individuo2 = copy.deepcopy(individuos[indice_max])
    del pontuacoes[indice_max]
    del individuos[indice_max]

    return individuo1, individuo2


def implementacao34_cont(palavra, alfabeto, alfabeto_indice, u, prob_deriva, N):
    size = len(palavra)
    individuos = []
    pontuacoes = []
    EPSILON = 1E-3
    for i in range(N):
        individuos.append(''.join(random.choice(alfabeto) for _ in range(size)))
        pontuacao = calcula_pontuacao(palavra, individuos[i], alfabeto_indice, u)
        pontuacoes.append(pontuacao)
    objetivo = calcula_pontuacao(palavra, palavra, alfabeto_indice, u)
    max_pontuacao = np.max(pontuacoes)
    melhor_individuo1, melhor_individuo2 = melhor_pontuacao_deriva(individuos, pontuacoes, prob_deriva)
    cont = 1
    while max_pontuacao < (objetivo - EPSILON):
        individuos.clear()
        pontuacoes.clear()
        for i in range(0, N, 2):
            novo_individuo1, novo_individuo2 = recombinacao(melhor_individuo1, melhor_individuo2)
            novo_individuo1 = mutacao(novo_individuo1, alfabeto, alfabeto_indice, u)
            novo_individuo2 = mutacao(novo_individuo2, alfabeto, alfabeto_indice, u)
            individuos.append(novo_individuo1)
            individuos.append(novo_individuo2)
            pontuacoes.append(calcula_pontuacao(palavra, novo_individuo1, alfabeto_indice, u))
            pontuacoes.append(calcula_pontuacao(palavra, novo_individuo2, alfabeto_indice, u))
        max_pontuacao = np.max(pontuacoes)
        melhor_individuo1, melhor_individuo2 = melhor_pontuacao_deriva(individuos, pontuacoes, prob_deriva)
        # print(melhor_individuo1, melhor_individuo2)
        # print(max_pontuacao, objetivo)
        # print(calcula_pontuacao(palavra, melhor_individuo1, alfabeto_indice, u), calcula_pontuacao(palavra, melhor_individuo2, alfabeto_indice, u))
        # print(pontuacoes)
        cont += 1
    return cont



def implementacao34():
    # u = np.array([[0.7, 0.1, 0.1, 0.1],[0.1, 0.7, 0.1, 0.1], [0.1, 0.1, 0.7, 0.1], [0.1, 0.1, 0.1, 0.7]])
    # u = np.array([[0.6, 0.05, 0.05, 0.3],[0.05, 0.6, 0.3, 0.05], [0.05, 0.3, 0.6, 0.05], [0.3, 0.05, 0.05, 0.6]])
    u = np.array([[0.7, 0.025, 0.025, 0.25], [0.025, 0.7, 0.25, 0.025], [0.025, 0.25, 0.7, 0.025], [0.25, 0.025, 0.025, 0.7]])
    # u = np.array([[0.5, 0.1, 0.1, 0.3],[0.1, 0.5, 0.3, 0.1], [0.1, 0.3, 0.5, 0.1], [0.3, 0.1, 0.1, 0.5]])

    palavra = carregar_palavra_base_dados('E.coli-sequence.txt', 15)
    alfabeto = ['a', 't', 'c', 'g']
    alfabeto_indice = {'a': 0, 't': 1, 'c': 2, 'g': 3}
    N = 10
    prob_deriva = 0.1

    distribuicao = []
    for _ in range(20):
        distribuicao.append(implementacao34_cont(palavra, alfabeto, alfabeto_indice, u, prob_deriva, N))

    print("Implementação 3.4:\nPara encontrar \"" + palavra + "\" com o alfabeto", alfabeto, "demorou em média",
          np.average(distribuicao), "tentativas, com desvio padrão", np.std(distribuicao))


def implementacao35_sim_populacao(palavra, individuo1, individuo2, alfabeto, alfabeto_indice, u, N):
    individuos = []
    pontuacoes = []
    for i in range(0, N, 2):
        novo_individuo1, novo_individuo2 = recombinacao(individuo1, individuo2)
        novo_individuo1 = mutacao(novo_individuo1, alfabeto, alfabeto_indice, u)
        novo_individuo2 = mutacao(novo_individuo2, alfabeto, alfabeto_indice, u)
        individuos.append(novo_individuo1)
        individuos.append(novo_individuo2)
        pontuacoes.append(calcula_pontuacao(palavra, novo_individuo1, alfabeto_indice, u))
        pontuacoes.append(calcula_pontuacao(palavra, novo_individuo2, alfabeto_indice, u))
    return individuos, pontuacoes


def seleciona_aleatoriamente(populacao, quant):
    selecionados = []
    for _ in range(quant):
        indice = int(np.round((len(populacao) - 1) * np.random.random_sample()))
        selecionados.append(copy.deepcopy(populacao[indice]))
        del populacao[indice]
    return selecionados


def elimina_piores(populacao, pontuacoes, quant):
    for _ in range(quant):
        indice_min = 0
        for i in range(1, len(pontuacoes)):
            try:
                if pontuacoes[i] < pontuacoes[indice_min]:
                    indice_min = i
            except:
                print(i, indice_min, len(populacao), len(pontuacoes), "\n", populacao, pontuacoes)
                exit()
        del pontuacoes[indice_min]
        del populacao[indice_min]



def implementacao35_cont(palavra, alfabeto, alfabeto_indice, u, prob_deriva, taxa_migracao, N):
    size = len(palavra)
    individuos = []
    pontuacoes = []
    EPSILON = 1E-3
    for i in range(N):
        individuos.append(''.join(random.choice(alfabeto) for _ in range(size)))
        pontuacao = calcula_pontuacao(palavra, individuos[i], alfabeto_indice, u)
        pontuacoes.append(pontuacao)
    objetivo = calcula_pontuacao(palavra, palavra, alfabeto_indice, u)
    max_pontuacao = np.max(pontuacoes)
    cont = 1
    while max_pontuacao < (objetivo - EPSILON):
        elimina_piores(individuos, pontuacoes, taxa_migracao)
        melhor_individuo1, melhor_individuo2 = melhor_pontuacao_deriva(individuos, pontuacoes, prob_deriva)
        for _ in range(0, taxa_migracao, 2):
            novo_individuo1, novo_individuo2 = recombinacao(melhor_individuo1, melhor_individuo2)
            novo_individuo1 = mutacao(novo_individuo1, alfabeto, alfabeto_indice, u)
            novo_individuo2 = mutacao(novo_individuo2, alfabeto, alfabeto_indice, u)
            individuos.append(novo_individuo1)
            individuos.append(novo_individuo2)
            pontuacoes.append(calcula_pontuacao(palavra, novo_individuo1, alfabeto_indice, u))
            pontuacoes.append(calcula_pontuacao(palavra, novo_individuo2, alfabeto_indice, u))
        individuos.append(melhor_individuo1)
        individuos.append(melhor_individuo2)
        pontuacoes.append(calcula_pontuacao(palavra, melhor_individuo1, alfabeto_indice, u))
        pontuacoes.append(calcula_pontuacao(palavra, melhor_individuo2, alfabeto_indice, u))
        max_pontuacao = np.max(pontuacoes)
        # print(melhor_individuo1, melhor_individuo2)
        # print(max_pontuacao, objetivo)
        # print(calcula_pontuacao(palavra, melhor_individuo1, alfabeto_indice, u), calcula_pontuacao(palavra, melhor_individuo2, alfabeto_indice, u))
        # print(pontuacoes)
        cont += 1
    return cont


def implementacao35():
    # u = np.array([[0.7, 0.1, 0.1, 0.1],[0.1, 0.7, 0.1, 0.1], [0.1, 0.1, 0.7, 0.1], [0.1, 0.1, 0.1, 0.7]])
    # u = np.array([[0.6, 0.05, 0.05, 0.3],[0.05, 0.6, 0.3, 0.05], [0.05, 0.3, 0.6, 0.05], [0.3, 0.05, 0.05, 0.6]])
    u = np.array([[0.7, 0.025, 0.025, 0.25], [0.025, 0.7, 0.25, 0.025], [0.025, 0.25, 0.7, 0.025], [0.25, 0.025, 0.025, 0.7]])
    # u = np.array([[0.5, 0.1, 0.1, 0.3],[0.1, 0.5, 0.3, 0.1], [0.1, 0.3, 0.5, 0.1], [0.3, 0.1, 0.1, 0.5]])

    palavra = carregar_palavra_base_dados('E.coli-sequence.txt', 7)
    alfabeto = ['a', 't', 'c', 'g']
    alfabeto_indice = {'a': 0, 't': 1, 'c': 2, 'g': 3}
    N = 10
    prob_deriva = 0.1
    taxa_migracao = int(np.round(0.8 * N))
    if taxa_migracao % 2 != 0:
        taxa_migracao += 1

    distribuicao = []
    for _ in range(1):
        distribuicao.append(implementacao35_cont(palavra, alfabeto, alfabeto_indice, u, prob_deriva, taxa_migracao, N))

    print("Implementação 3.5:\nPara encontrar \"" + palavra + "\" com o alfabeto", alfabeto, "demorou em média",
          np.average(distribuicao), "tentativas, com desvio padrão", np.std(distribuicao))