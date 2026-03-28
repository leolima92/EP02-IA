from problema import (
    TURNOS,
    POSTOS,
    BAIRROS,
    FROTA_TOTAL,
    MIN_AMB_POSTO,
    MAX_AMB_POSTO,
    CAPACIDADE_ATENDIMENTO_POR_AMB,
    PESOS_TURNOS,
    POSTOS_ATENDEM_BAIRROS,
    BAIRROS_COBERTOS_POR_POSTOS,
    BAIRROS_DADOS,
    DEMANDA_BAIRROS,
    PENALIDADES,
    GAMMA_DEFICIT,
    BAIRROS_CRITICOS_R7,
    POSTOS_CRITICOS_R7,
    POPULACAO_TOTAL,
    INDICE_POSTO,
    INDICE_TURNO
)



def ambulancias_posto(individuo, posto, turno):
    i_posto = INDICE_POSTO[posto]
    i_turno = INDICE_TURNO[turno]
    return individuo[i_posto][i_turno]


def capacidade_posto(individuo, posto, turno):
    qtd_ambulancias = ambulancias_posto(individuo, posto, turno)
    return qtd_ambulancias * CAPACIDADE_ATENDIMENTO_POR_AMB


def demanda_posto(posto, turno):
    total = 0
    for bairro in POSTOS_ATENDEM_BAIRROS[posto]:
        total += DEMANDA_BAIRROS[bairro][turno]
    return total


def bairro_coberto(individuo, bairro, turno):
    for posto in BAIRROS_COBERTOS_POR_POSTOS[bairro]:
        if ambulancias_posto(individuo, posto, turno) > 0:
            return True
    return False


def calcular_cobertura_populacional(individuo):
    cobertura_ponderada_total = 0
    cobertura_turno = {}

    for turno in TURNOS:
        populacao_coberta = 0

        for bairro in BAIRROS:
            if bairro_coberto(individuo, bairro, turno):
                populacao_coberta += BAIRROS_DADOS[bairro]["pop"]

        percentual = (populacao_coberta / POPULACAO_TOTAL) * 100
        cobertura_turno[turno] = {
            "populacao_coberta": populacao_coberta,
            "percentual": percentual
        }

        cobertura_ponderada_total += populacao_coberta * PESOS_TURNOS[turno]

    return cobertura_ponderada_total, cobertura_turno



def calcular_deficit(individuo):
    deficit_total = 0
    deficit_detalhado = {}

    for posto in POSTOS:
        deficit_detalhado[posto] = {}

        for turno in TURNOS:
            dem = demanda_posto(posto, turno)
            cap = capacidade_posto(individuo, posto, turno)
            deficit = max(0, dem - cap)

            deficit_detalhado[posto][turno] = deficit
            deficit_total += deficit

    return deficit_total, deficit_detalhado



def verificar_restricoes(individuo):
    violacoes = {
        "R1_FROTA": 0,
        "R2_MINIMO": 0,
        "R3_MAXIMO": 0,
        "R4_COBERTURA": 0,
        "R5_ALTA_DEMANDA": 0,
        "R6_RODIZIO": 0,
        "R7_NOTURNO_CRITICO": 0
    }

    # R1 - soma por turno deve ser 15
    for turno in TURNOS:
        soma_turno = 0
        for posto in POSTOS:
            soma_turno += ambulancias_posto(individuo, posto, turno)

        if soma_turno != FROTA_TOTAL:
            violacoes["R1_FROTA"] += 1

    # R2 - mínimo 1 por posto
    for posto in POSTOS:
        for turno in TURNOS:
            if ambulancias_posto(individuo, posto, turno) < MIN_AMB_POSTO:
                violacoes["R2_MINIMO"] += 1

    # R3 - máximo 4 por posto
    for posto in POSTOS:
        for turno in TURNOS:
            if ambulancias_posto(individuo, posto, turno) > MAX_AMB_POSTO:
                violacoes["R3_MAXIMO"] += 1

    # R4 - todo bairro deve estar coberto em todo turno
    for bairro in BAIRROS:
        for turno in TURNOS:
            if not bairro_coberto(individuo, bairro, turno):
                violacoes["R4_COBERTURA"] += 1

    # R5 - posto com demanda > 10 deve ter pelo menos 2 ambulâncias
    for posto in POSTOS:
        for turno in TURNOS:
            if demanda_posto(posto, turno) > 10 and ambulancias_posto(individuo, posto, turno) < 2:
                violacoes["R5_ALTA_DEMANDA"] += 1

    # R6 - não pode repetir a mesma quantidade nos 3 turnos
    for posto in POSTOS:
        m = ambulancias_posto(individuo, posto, "Manhã")
        t = ambulancias_posto(individuo, posto, "Tarde")
        n = ambulancias_posto(individuo, posto, "Noite")

        if m == t == n:
            violacoes["R6_RODIZIO"] += 1

    # R7 - reforço noturno nos postos críticos
    total_amb_noite_criticos = sum(
        ambulancias_posto(individuo, posto, "Noite")
        for posto in POSTOS_CRITICOS_R7
    )

    if total_amb_noite_criticos < 2:
        violacoes["R7_NOTURNO_CRITICO"] += 1

    return violacoes


def calcular_penalidade_total(violacoes):

    penalidade_total = 0

    for restricao, qtd_violacoes in violacoes.items():
        penalidade_total += PENALIDADES[restricao] * qtd_violacoes

    return penalidade_total


def calcular_fitness(individuo):
    cobertura_ponderada, cobertura_por_turno = calcular_cobertura_populacional(individuo)
    deficit_total, deficit_detalhado = calcular_deficit(individuo)
    violacoes = verificar_restricoes(individuo)
    penalidade_total = calcular_penalidade_total(violacoes)

    fitness = cobertura_ponderada - (deficit_total * GAMMA_DEFICIT) - penalidade_total

    return {
        "fitness": fitness,  
        "cobertura_ponderada": cobertura_ponderada,
        "cobertura_por_turno": cobertura_por_turno,
        "deficit_total": deficit_total,
        "deficit_detalhado": deficit_detalhado,
        "violacoes": violacoes,
        "penalidade_total": penalidade_total,
        "total_violacoes": sum(violacoes.values()) 
    }


if __name__ == "__main__":
    individuo_teste = [
        [2, 2, 1],  # P1
        [2, 2, 1],  # P2
        [2, 3, 2],  # P3
        [2, 2, 2],  # P4
        [2, 2, 2],  # P5
        [1, 1, 1],  # P6
        [2, 2, 3],  # P7
        [2, 1, 3]   # P8
    ]

    resultado = calcular_fitness(individuo_teste)

    print("Fitness:", resultado["fitness"])
    print("Cobertura ponderada:", resultado["cobertura_ponderada"])
    print("Déficit total:", resultado["deficit_total"])
    print("Penalidade total:", resultado["penalidade_total"])
    print("Violações:", resultado["violacoes"])
    print("Cobertura por turno:", resultado["cobertura_por_turno"])
    print("Déficit detalhado:", resultado["deficit_detalhado"])