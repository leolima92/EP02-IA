import random
import copy

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

    
    pass