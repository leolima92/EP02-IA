
# Otimização de Alocação de Ambulâncias - Algoritmo Genético (EP02-IA)

Este projeto implementa um **Algoritmo Genético (AG)** para resolver o problema de otimização de alocação de uma frota de 15 ambulâncias em 8 postos de atendimento, visando cobrir 12 bairros e atender a demanda de 3 turnos diários.

O objetivo é encontrar uma alocação eficiente que **maximize a cobertura populacional** e **minimize o déficit de atendimento**, respeitando rigorosamente as restrições operacionais.



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
    

##  Função de Fitness

A qualidade de cada indivíduo é avaliada pela fórmula:

$$Fitness = CP - (DT \cdot  \gamma) - \sum P_i$$

Onde cada ambulância possui capacidade de atender até **16 ocorrências por turno**. As penalidades são aplicadas conforme a gravidade da restrição violada, garantindo que a evolução priorize soluções viáveis.