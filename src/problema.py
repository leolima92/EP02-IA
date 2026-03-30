"""
Modelagem do problema de otimização de alocação de ambulâncias
utilizando Algoritmo Genético.

definição do problema:
- dados
- parâmetros
- restrições
- estrutura do indivíduo

"""

# parametros operacionais
NUM_POSTOS = 8
NUM_TURNOS = 3
FROTA_TOTAL = 15
MIN_AMB_POSTO = 1
MAX_AMB_POSTO = 4
CAPACIDADE_ATENDIMENTO_POR_AMB = 16

# configs
TAMANHO_POPULACAO = 100  # soluções testadas por vez
GERACOES = 200           # qtd de ciclos de evolução
TAXA_CROSSOVER = 0.8     # prob de combinação de soluções 
TAXA_MUTACAO = 0.05      # prob de transferencia de ambulâncias entre postos

# dados do problema
TURNOS = ["Manhã", "Tarde", "Noite"]
POSTOS = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"]
BAIRROS = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "B11", "B12"]

PESOS_TURNOS = {"Manhã": 1.0, "Tarde": 1.2, "Noite": 1.5}

# mapeamento de bairros atendidos por cada posto
POSTOS_ATENDEM_BAIRROS = {
    "P1": ["B1", "B2", "B7"], "P2": ["B2", "B3", "B5"],
    "P3": ["B3", "B4", "B6"], "P4": ["B4", "B8", "B9"],
    "P5": ["B6", "B9", "B10"], "P6": ["B5", "B7", "B11"],
    "P7": ["B10", "B11", "B12"], "P8": ["B8", "B11", "B12"]
}

# dados demográficos
BAIRROS_DADOS = {
    "B1":  {"pop": 18000}, "B2":  {"pop": 25000}, "B3":  {"pop": 30000},
    "B4":  {"pop": 22000}, "B5":  {"pop": 15000}, "B6":  {"pop": 28000},
    "B7":  {"pop": 12000}, "B8":  {"pop": 20000}, "B9":  {"pop": 35000},
    "B10": {"pop": 40000}, "B11": {"pop": 18000}, "B12": {"pop": 32000}
}

# ocorrencia de bairro por turno
DEMANDA_BAIRROS = {
    "B1": {"Manhã": 3, "Tarde": 4, "Noite": 2}, "B2": {"Manhã": 4, "Tarde": 5, "Noite": 2},
    "B3": {"Manhã": 5, "Tarde": 6, "Noite": 3}, "B4": {"Manhã": 3, "Tarde": 4, "Noite": 2},
    "B5": {"Manhã": 2, "Tarde": 3, "Noite": 1}, "B6": {"Manhã": 4, "Tarde": 5, "Noite": 3},
    "B7": {"Manhã": 2, "Tarde": 2, "Noite": 1}, "B8": {"Manhã": 3, "Tarde": 4, "Noite": 2},
    "B9": {"Manhã": 5, "Tarde": 7, "Noite": 4}, "B10": {"Manhã": 6, "Tarde": 8, "Noite": 4},
    "B11": {"Manhã": 3, "Tarde": 4, "Noite": 2}, "B12": {"Manhã": 5, "Tarde": 6, "Noite": 3}
}

# processamento automatico
BAIRROS_COBERTOS_POR_POSTOS = {b: [p for p, brs in POSTOS_ATENDEM_BAIRROS.items() if b in brs] for b in BAIRROS}
INDICE_POSTO = {p: i for i, p in enumerate(POSTOS)}
INDICE_TURNO = {t: i for i, t in enumerate(TURNOS)}
POPULACAO_TOTAL = sum(d["pop"] for d in BAIRROS_DADOS.values())

# penalidades do fitness
PENALIDADES = {
    "R1_FROTA": 100000, "R2_MINIMO": 100000, "R3_MAXIMO": 20000,
    "R4_COBERTURA": 100000, "R5_ALTA_DEMANDA": 5000,
    "R6_RODIZIO": 2000, "R7_NOTURNO_CRITICO": 5000
}
GAMMA_DEFICIT = 150  # fator de penalidade para o déficit
BAIRROS_CRITICOS_R7 = ["B9", "B10"] 
POSTOS_CRITICOS_R7 = ["P4", "P5", "P7"]


if __name__ == "__main__":
    print(f"Problema carregado. População total: {POPULACAO_TOTAL} habitantes.")