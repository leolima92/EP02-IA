import random
import copy
from problema import NUM_POSTOS, NUM_TURNOS, MIN_AMB_POSTO, MAX_AMB_POSTO

def mutacao(individuo, taxa_mutacao=0.1): 
    # Verifica se a mutação deve ocorrer com base na taxa
    if random.random() > taxa_mutacao:
        return individuo

    # Cria uma cópia para não alterar o objeto original
    novo_individuo = copy.deepcopy(individuo)
    matriz = novo_individuo['cromossomo']

    # Seleciona um turno aleatório (coluna da matriz: 0, 1 ou 2)
    turno_escolhido = random.randint(0, NUM_TURNOS - 1)

    # Identifica postos que podem DOAR (devem ter > 1 ambulância para respeitar R2)
    postos_doadores = [
        p for p in range(NUM_POSTOS) 
        if matriz[p][turno_escolhido] > MIN_AMB_POSTO
    ]

    # Identifica postos que podem RECEBER (devem ter < 4 ambulâncias para respeitar R3)
    postos_receptores = [
        p for p in range(NUM_POSTOS) 
        if matriz[p][turno_escolhido] < MAX_AMB_POSTO
    ]

    # Tenta realizar a transferência
    if postos_doadores and postos_receptores:
        posto_origem = random.choice(postos_doadores) 
        posto_destino = random.choice(postos_receptores)

        # Garante que não estamos movendo para o mesmo posto
        if posto_origem != posto_destino:
            matriz[posto_origem][turno_escolhido] -= 1
            matriz[posto_destino][turno_escolhido] += 1
            
            # Remove o fitness antigo para que o 'main' saiba que precisa recalcular
            if 'fitness' in novo_individuo:
                del novo_individuo['fitness']
            if 'detalhes' in novo_individuo:
                del novo_individuo['detalhes']

    return novo_individuo