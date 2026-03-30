O objetivo é encontrar uma alocação eficiente de ambulâncias entre postos de atendimento ao longo de três turnos do dia, utilizando um **Algoritmo Genético (AG)**.

A solução busca **maximizar a cobertura populacional** e **minimizar o déficit de atendimento**, respeitando diversas restrições operacionais.

---

# Descrição do Problema

A cidade possui:

- **12 bairros**
- **8 postos de atendimento**
- **15 ambulâncias disponíveis**

O dia é dividido em **3 turnos**:

| Turno | Horário |
|------|------|
| Manhã | 06h – 14h |
| Tarde | 14h – 22h |
| Noite | 22h – 06h |

O objetivo é decidir **quantas ambulâncias devem ficar em cada posto em cada turno**.

Cada ambulância consegue atender **até 16 ocorrências por turno**.

---

# Representação da Solução

Cada solução (indivíduo) é representada por uma **matriz 8 × 3**:

- linhas → postos
- colunas → turnos

Exemplo:

```

Posto | Manhã | Tarde | Noite
P1    |   2   |   2   |   1
P2    |   2   |   2   |   1
P3    |   2   |   3   |   2
P4    |   2   |   2   |   2
P5    |   2   |   2   |   2
P6    |   1   |   1   |   1
P7    |   2   |   2   |   3
P8    |   2   |   1   |   3

```

Cada coluna deve somar **15 ambulâncias**, que é o total disponível.

---

# Restrições do Problema

O algoritmo deve respeitar as seguintes regras:

**R1 – Frota total fixa**  
A soma de ambulâncias por turno deve ser igual a 15.

**R2 – Mínimo por posto**  
Cada posto deve ter pelo menos 1 ambulância.

**R3 – Máximo por posto**  
Cada posto pode ter no máximo 4 ambulâncias.

**R4 – Cobertura mínima**  
Todos os bairros devem estar cobertos por pelo menos um posto com ambulância.

**R5 – Alta demanda**  
Postos que atendem mais de 10 ocorrências por turno devem ter pelo menos 2 ambulâncias.

**R6 – Rodízio de equipes**  
Um posto não pode ter a mesma quantidade de ambulâncias nos três turnos.

**R7 – Reforço noturno**  
Os bairros críticos (B9 e B10) precisam de reforço noturno nos postos P4, P5 e P7.

---

# Função de Fitness

A qualidade de cada solução é calculada considerando:

1. **Cobertura populacional ponderada**

Bairros cobertos geram pontos proporcionais à população e ao peso do turno.

Pesos dos turnos:

| Turno | Peso |
|------|------|
| Manhã | 1.0 |
| Tarde | 1.2 |
| Noite | 1.5 |

---

2. **Déficit de atendimento**

Caso a demanda seja maior que a capacidade do posto:

```

deficit = max(0, demanda - capacidade)

```

Cada ambulância atende até **16 ocorrências por turno**.

---

3. **Penalidades por violação de restrições**

Restrições críticas recebem penalidades maiores.

A função final é:

```

fitness = cobertura

* (deficit × gamma)
* penalidades

```

---

# Estrutura do Projeto

```

EP02-IA/
│
├── problema.py
├── fitness.py
└── README.md

```

### problema.py

Contém a definição completa do problema:

- postos
- bairros
- demanda
- cobertura
- parâmetros
- penalidades

---

### fitness.py

Implementa as funções de avaliação de uma solução:

- cálculo da cobertura populacional
- cálculo do déficit de atendimento
- verificação das restrições
- cálculo das penalidades
- cálculo do fitness final

---


