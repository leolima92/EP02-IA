from problema import (
    POSTOS,
    TURNOS,
    FROTA_TOTAL,
    MIN_AMB_POSTO,
    MAX_AMB_POSTO,
)
import random

def gerar_individuo():
    num_postos = len(POSTOS)
    num_turnos = len(TURNOS)
    
    individuo = [
        [MIN_AMB_POSTO for _ in range(num_turnos)]
        for _ in range(num_postos)
    ]
    
    for i_turno in range(num_turnos):
        ambulancias_alocadas = num_postos * MIN_AMB_POSTO
        restante = FROTA_TOTAL - ambulancias_alocadas
        
        while restante > 0:
            i_posto = random.randint(0, num_postos - 1)
            if individuo[i_posto][i_turno] < MAX_AMB_POSTO:
                individuo[i_posto][i_turno] += 1
                restante -= 1
    return individuo

def gerar_populacao(tamanho_populacao):
    populacao = []

    for _ in range(tamanho_populacao):
        individuo = gerar_individuo()
        populacao.append(individuo)

    return populacao