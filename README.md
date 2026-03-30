
# Otimização de Alocação de Ambulâncias - Algoritmo Genético (EP02-IA)

Este projeto implementa um **Algoritmo Genético (AG)** para resolver o problema de otimização de alocação de uma frota de 15 ambulâncias em 8 postos de atendimento, visando cobrir 12 bairros e atender a demanda de 3 turnos diários.

O objetivo é encontrar uma alocação eficiente que **maximize a cobertura populacional** e **minimize o déficit de atendimento**, respeitando rigorosamente as restrições operacionais.

A solução busca **maximizar a cobertura populacional** e **minimizar o déficit de atendimento**, respeitando diversas restrições operacionais.



## Como Executar

O sistema foi desenvolvido em **Python**. Certifique-se de estar na pasta raiz do projeto (`EP02-IA`) ao executar os comandos.

1. **Execução Padrão:**
```bash
   python src/main.py --populacao 100 --geracoes 100 --mutacao 0.10 --crossover 0.80
```

2.  **Parâmetros Customizados via CLI:**
    
    -   `--populacao`: Tamanho da população (padrão: 100)
        
    -   `--geracoes`: Número de gerações (padrão: 100)
        
    -   `--mutacao`: Taxa de mutação [0.0 - 1.0] (padrão: 0.1)
        
    -   `--crossover`: Taxa de crossover [0.0 - 1.0] (padrão: 0.8)
 


## Descrição do Problema

A cidade possui **12 bairros** (295.000 hab.), **8 postos** e **15 ambulâncias**. O dia é dividido em:

-   **Manhã:** 06h – 14h (Peso 1.0)
    
-   **Tarde:** 14h – 22h (Peso 1.2)
    
-   **Noite:** 22h – 06h (Peso 1.5)
    

### Restrições Implementadas (R1 a R7)

-   **R1:** Frota total fixa de 15 ambulâncias por turno.
    
-   **R2/R3:** Mínimo de 1 e máximo de 4 ambulâncias por posto.
    
-   **R4:** Cobertura obrigatória de todos os bairros.
    
-   **R5:** Alocação proporcional em postos com demanda > 10 ocorrências.
    
-   **R6:** Obrigatoriedade de rodízio/variação de frota entre turnos.
    
-   **R7:** Reforço noturno obrigatório para os bairros críticos (B9 e B10).
    
## Representação da Solução

Cada solução (indivíduo) é representada por uma **matriz 8 × 3**:

- Linhas → Postos
- Colunas → Turnos

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

##  Função de Fitness

A qualidade de cada indivíduo é avaliada pela fórmula:

$$Fitness = CP - (DT \cdot  \gamma) - \sum P_i$$

Onde cada ambulância possui capacidade de atender até **16 ocorrências por turno**. As penalidades são aplicadas conforme a gravidade da restrição violada, garantindo que a evolução priorize soluções viáveis.

## Deficiência de Atendimento

O déficit de atendimento ocorre sempre que a demanda por ocorrências em um determinado posto e turno supera a capacidade das ambulâncias alocadas para aquele mesmo local e período.

A capacidade de um posto é calculada multiplicando o número de ambulâncias alocadas pela capacidade de cada uma (16 ocorrências/turno). O déficit para cada posto p e turno t é calculado pela fórmula:

$$Deficit_{p,t} = \max(0, Demanda_{p,t} - Capacidade_{p,t})$$

O déficit total do indivíduo é a soma dos déficits de todos os postos em todos os turnos. Esse valor é multiplicado por um fator de peso de déficit (gamma) para penalizar soluções ineficientes.

## Penalidade por violação das restrições

A penalidade total ($\sum P_i$) é calculada multiplicando a quantidade de violações de cada restrição pelo seu peso de penalidade (definido no arquivo problema.py).

# Saída esperada

Segue um exemplo de saída esperada do problema, lembrando que os dados podem variar pois os parâmetros são configuráveis. O exemplo a seguir foi realizado utilizando a forma de execução padrão

```
Geração   0 | Mínimo: 1043600.00 | Média: 1062498.00 | Máximo: 1079500.00 | Violações: {'R1_FROTA': 0, 'R2_MINIMO': 0, 'R3_MAXIMO': 0, 'R4_COBERTURA': 0, 'R5_ALTA_DEMANDA': 2, 'R6_RODIZIO': 1, 'R7_NOTURNO_CRITICO': 0}

# todas as outras gerações ....

Geração  99 | Mínimo: 1086200.00 | Média: 1091027.00 | Máximo: 1091500.00 | Violações: {'R1_FROTA': 0, 'R2_MINIMO': 0, 'R3_MAXIMO': 0, 'R4_COBERTURA': 0, 'R5_ALTA_DEMANDA': 0, 'R6_RODIZIO': 0, 'R7_NOTURNO_CRITICO': 0}

Melhor Solução Encontrada:
==================================================
Posto | Manhã | Tarde | Noite
 P1   |   1   |   2   |   3
 P2   |   2   |   2   |   3
 P3   |   3   |   2   |   1
 P4   |   2   |   2   |   1
 P5   |   2   |   2   |   3
 P6   |   1   |   1   |   2
 P7   |   2   |   2   |   1
 P8   |   2   |   2   |   1
--------------------------------------------------
Fitness Final: 1091500.00
Déficit Total de Ocorrências: 0
Violações de Restrições: {'R1_FROTA': 0, 'R2_MINIMO': 0, 'R3_MAXIMO': 0, 'R4_COBERTURA': 0, 'R5_ALTA_DEMANDA': 0, 'R6_RODIZIO': 0, 'R7_NOTURNO_CRITICO': 0}  
Cobertura Manhã: 100.0% da população
Cobertura Tarde: 100.0% da população
Cobertura Noite: 100.0% da população

```

# Estrutura do Projeto

```

EP02-IA/
├── docs/
│   ├── hiperparametros.md
│   └── modelagem.md
├── src/
│   ├── crossover.py
│   ├── fitness.py
│   ├── gerador.py
│   ├── main.py
│   ├── mutacao.py
│   ├── problema.py
│   └── selecao.py
├── .gitignore
└── README.md

```