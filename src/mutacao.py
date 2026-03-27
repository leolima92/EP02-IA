import random
import copy
from problema import NUM_POSTOS, NUM_TURNOS, MIN_AMB_POSTO, MAX_AMB_POSTO

def mutacao(individuo, taxa_mutacao=0.1): 
    if random.random() > taxa_mutacao:
        return individuo

    #cria uma cópia para não alterar o objeto original
    novo_individuo = copy.deepcopy(individuo)
    matriz = novo_individuo['cromossomo']

    #seleciona um turno aleatório 
    turno_escolhido = random.randint(0, NUM_TURNOS - 1)

    #identifica postos que podem DOAR (devem ter > 1 ambulância para respeitar R2)
    postos_doadores = [
        p for p in range(NUM_POSTOS) 
        if matriz[p][turno_escolhido] > MIN_AMB_POSTO
    ]

    #identifica postos que podem RECEBER (devem ter < 4 ambulâncias para respeitar R3)
    postos_receptores = [
        p for p in range(NUM_POSTOS) 
        if matriz[p][turno_escolhido] < MAX_AMB_POSTO
    ]

    # tentativa de transferencia
    if postos_doadores and postos_receptores:
        posto_origem = random.choice(postos_doadores) 
        posto_destino = random.choice(postos_receptores)

        
        if posto_origem != posto_destino:
            matriz[posto_origem][turno_escolhido] -= 1
            matriz[posto_destino][turno_escolhido] += 1
            
            # remoção do fitness antigo
            if 'fitness' in novo_individuo:
                del novo_individuo['fitness']
            if 'detalhes' in novo_individuo:
                del novo_individuo['detalhes']

    return novo_individuo