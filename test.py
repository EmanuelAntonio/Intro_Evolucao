def hardy_weinberg_selection(p, q, s, generations):
    frequency_changes = []
    for _ in range(generations):
        q = (1 - s) * q  # Frequência do alelo 'a' na próxima geração após a seleção

        p = 1 - q  # Frequência do alelo 'A' na próxima geração

        frequency_changes.append(q)  # Registro da frequência do alelo 'a'

    return frequency_changes


# Configurações iniciais
p = 1  # Frequência inicial do alelo 'A'
q = 0  # Frequência inicial do alelo 'a'
generations = 100  # Número de gerações

# Coeficientes de seleção
s1 = 0.05  # Fator de sobrevivência 1
s2 = 0.01  # Fator de sobrevivência 2

# Simulação com coeficiente de seleção s = 0.05
frequency_changes_1 = hardy_weinberg_selection(p, q, s1, generations)

# Simulação com coeficiente de seleção s = 0.01
frequency_changes_2 = hardy_weinberg_selection(p, q, s2, generations)

# Exibição das mudanças na frequência gênica
print("Mudanças na frequência gênica com coeficiente de seleção s = 0.05:")
for generation, frequency in enumerate(frequency_changes_1):
    print(f"Geração {generation + 1}: Frequência do alelo 'a': {frequency}")

print("\nMudanças na frequência gênica com coeficiente de seleção s = 0.01:")
for generation, frequency in enumerate(frequency_changes_2):
    print(f"Geração {generation + 1}: Frequência do alelo 'a': {frequency}")
print("teste")