import random
import copy

# essa função faz o crossover uniforme trocando as colunas entre os pais 
# **futuramente no main tem que fazer a checagem se o individuo tem fitness, se não tiver ele é novo** <- importante
# se tiver fitness ele não sofreu crossover
#tem 30% de chance de não haver crossover
#tem 25% de chance de crossover com os filhos iguais aos pais

def crossover_uniforme(pai1, pai2, taxa_crossover=0.7):
    matriz_pai1 = pai1['cromossomo'] #matrizes dos pais
    matriz_pai2 = pai2['cromossomo']

    if(random.random() > taxa_crossover): #nao houve crossover
        return  copy.deepcopy(pai1), copy.deepcopy(pai2) 
    
    num_linhas = len(matriz_pai1) # postos
    num_colunas = len(matriz_pai1[0]) # turnos

    matriz_filho1 = []
    for _ in range(num_linhas):
        linha = []
        for _ in range(num_colunas):
            linha.append(0)
        matriz_filho1.append(linha)

    matriz_filho2 = []
    for _ in range(num_linhas):
        linha = []
        for _ in range(num_colunas):
            linha.append(0)
        matriz_filho2.append(linha)

    for i in range(num_colunas): # i = coluna/turno e j = linha/postos
        if random.random() < 0.5:
            for j in range(num_linhas):
                matriz_filho1[j][i] = matriz_pai1[j][i]
                matriz_filho2[j][i] = matriz_pai2[j][i]
        else:
            for j in range(num_linhas):
                matriz_filho1[j][i] = matriz_pai2[j][i]
                matriz_filho2[j][i] = matriz_pai1[j][i]
    
    return {'cromossomo': matriz_filho1}, {'cromossomo': matriz_filho2}