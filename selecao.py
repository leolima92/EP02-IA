import random
from fitness import calcular_fitness


def selecionar_por_torneio(populacao, k =3):
    if not populacao:
        raise ValueError("A população não pode ser vazia.")
    
    if k <= 0:
        raise ValueError("O número de competidores (k) deve ser maior que zero.")
    
    if k > len(populacao):
        k = len(populacao)

    candidatos = random.sample(populacao, k)
    melhor = max(candidatos, key=lambda ind: calcular_fitness(ind)["fitness"])
    
    return melhor

def selecionar_por_pais(populacao, k = 3):
    pai1 = selecionar_por_torneio(populacao, k)
    pai2 = selecionar_por_torneio(populacao, k)
    return pai1, pai2


if __name__ == "__main__":
    from gerador import gerar_populacao

    populacao = gerar_populacao(10)

    pai1, pai2 = selecionar_por_pais(populacao, k=3)

    print("Pai 1:")
    for linha in pai1:
        print(linha)

    print("\nPai 2:")
    for linha in pai2:
        print(linha)
        
        


"""
Seleção por torneio para o Algoritmo Genético.

- Sorteia k indivíduos da população
- Escolhe o de maior fitness
- Permite selecionar dois pais para reprodução
"""