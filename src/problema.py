"""
Modelagem do problema de otimização de alocação de ambulâncias
utilizando Algoritmo Genético.

definição do problema:
- dados
- parâmetros
- restrições
- estrutura do indivíduo

"""


NUM_POSTOS = 8
NUM_TURNOS = 3
FROTA_TOTAL = 15

MIN_AMB_POSTO = 1
MAX_AMB_POSTO = 4
CAPACIDADE_ATENDIMENTO_POR_AMB = 16

TURNOS = ["Manhã", "Tarde", "Noite"]
POSTOS = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"]
BAIRROS = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "B11", "B12"]

PESOS_TURNOS = {
    "Manhã": 1.0,
    "Tarde": 1.2,
    "Noite": 1.5
}

# POSTOS DE ATENDIMENTO


POSTOS_COORD = {
    "P1": (2, 8),
    "P2": (5, 15),
    "P3": (10, 10),
    "P4": (15, 5),
    "P5": (18, 14),
    "P6": (8, 20),
    "P7": (20, 20),
    "P8": (14, 25)
}

# Cobertura oficial
POSTOS_ATENDEM_BAIRROS = {
    "P1": ["B1", "B2", "B7"],
    "P2": ["B2", "B3", "B5"],
    "P3": ["B3", "B4", "B6"],
    "P4": ["B4", "B8", "B9"],
    "P5": ["B6", "B9", "B10"],
    "P6": ["B5", "B7", "B11"],
    "P7": ["B10", "B11", "B12"],
    "P8": ["B8", "B11", "B12"]
}


# BAIRROS
BAIRROS_DADOS = {
    "B1":  {"pop": 18000, "centroide": (1, 7)},
    "B2":  {"pop": 25000, "centroide": (4, 12)},
    "B3":  {"pop": 30000, "centroide": (8, 14)},
    "B4":  {"pop": 22000, "centroide": (12, 7)},
    "B5":  {"pop": 15000, "centroide": (6, 18)},
    "B6":  {"pop": 28000, "centroide": (11, 12)},
    "B7":  {"pop": 12000, "centroide": (4, 18)},
    "B8":  {"pop": 20000, "centroide": (13, 3)},
    "B9":  {"pop": 35000, "centroide": (17, 8)},
    "B10": {"pop": 40000, "centroide": (20, 12)},
    "B11": {"pop": 18000, "centroide": (16, 22)},
    "B12": {"pop": 32000, "centroide": (22, 18)}
}

DEMANDA_BAIRROS = {
    "B1":  {"Manhã": 3, "Tarde": 4, "Noite": 2},
    "B2":  {"Manhã": 4, "Tarde": 5, "Noite": 2},
    "B3":  {"Manhã": 5, "Tarde": 6, "Noite": 3},
    "B4":  {"Manhã": 3, "Tarde": 4, "Noite": 2},
    "B5":  {"Manhã": 2, "Tarde": 3, "Noite": 1},
    "B6":  {"Manhã": 4, "Tarde": 5, "Noite": 3},
    "B7":  {"Manhã": 2, "Tarde": 2, "Noite": 1},
    "B8":  {"Manhã": 3, "Tarde": 4, "Noite": 2},
    "B9":  {"Manhã": 5, "Tarde": 7, "Noite": 4},
    "B10": {"Manhã": 6, "Tarde": 8, "Noite": 4},
    "B11": {"Manhã": 3, "Tarde": 4, "Noite": 2},
    "B12": {"Manhã": 5, "Tarde": 6, "Noite": 3}
}


# MAPEAMENTO REVERSO

BAIRROS_COBERTOS_POR_POSTOS = {bairro: [] for bairro in BAIRROS}

for posto, bairros_cobertos in POSTOS_ATENDEM_BAIRROS.items():
    for bairro in bairros_cobertos:
        BAIRROS_COBERTOS_POR_POSTOS[bairro].append(posto)


# RESTRIÇÕES DO PROBLEMA

RESTRICOES = {
    "R1": "A soma de ambulâncias em cada turno deve ser exatamente 15.",
    "R2": "Cada posto deve ter pelo menos 1 ambulância por turno.",
    "R3": "Cada posto pode ter no máximo 4 ambulâncias por turno.",
    "R4": "Cada bairro deve estar coberto por pelo menos 1 posto com ambulância em cada turno.",
    "R5": "Postos com demanda total acima de 10 ocorrências no turno devem ter pelo menos 2 ambulâncias.",
    "R6": "Nenhum posto pode ter a mesma quantidade de ambulâncias nos 3 turnos consecutivos.",
    "R7": "No turno da noite, os bairros B9 e B10 devem ter cobertura reforçada de pelo menos 2 ambulâncias nos postos que os atendem."
}



PENALIDADES = {
    "R1_FROTA": 100000,
    "R2_MINIMO": 100000,
    "R3_MAXIMO": 20000,
    "R4_COBERTURA": 100000,
    "R5_ALTA_DEMANDA": 5000,
    "R6_RODIZIO": 2000,
    "R7_NOTURNO_CRITICO": 5000
}

GAMMA_DEFICIT = 150

BAIRROS_CRITICOS_R7 = ["B9", "B10"]
POSTOS_CRITICOS_R7 = ["P4", "P5", "P7"]


INDICE_POSTO = {posto: i for i, posto in enumerate(POSTOS)}
INDICE_TURNO = {turno: i for i, turno in enumerate(TURNOS)}



POPULACAO_TOTAL = sum(BAIRROS_DADOS[bairro]["pop"] for bairro in BAIRROS)


if __name__ == "__main__":
    print("POSTOS E BAIRROS COBERTOS")
    for posto, bairros in POSTOS_ATENDEM_BAIRROS.items():
        print(f"{posto}: {bairros}")

    print("\n BAIRROS E POSTOS QUE OS COBREM")
    for bairro, postos in BAIRROS_COBERTOS_POR_POSTOS.items():
        print(f"{bairro}: {postos}")

    print("\n DEMANDA POR BAIRRO")
    for bairro, demanda in DEMANDA_BAIRROS.items():
        print(f"{bairro}: {demanda}")

    print(f"\nPopulação total: {POPULACAO_TOTAL}")