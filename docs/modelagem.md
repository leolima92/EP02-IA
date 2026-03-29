
# Documentação Técnica: Otimização de Alocação de Ambulâncias (EP02-IA)

Este documento detalha a modelagem do problema de alocação de frotas utilizando Algoritmos Genéticos, para otimizar o atendimento em 12 bairros através de 8 postos.

---

## 1. Cromossomo

O cromossomo representa a escala de alocação da frota de 15 ambulâncias ao longo do dia.

* **Estrutura:** Matriz de inteiros de dimensões $8 \ postos \times 3 \ turnos$ 
* **Representação do Gene:** Cada célula $a_{p,t}$ armazena a quantidade de ambulâncias no posto $p$ durante o turno $t$.
* **Domínio e Espaço de Busca:** Cada gene assume valores no intervalo $[1, 4]$, respeitando as restrições físicas de cada posto.
    * O tamanho total é de 24 genes.

## 2. Função de Aptidão (Fitness)

A função de aptidão foi modelada para equilibrar a cobertura máxima da população com a eficiência no atendimento (mínimo déficit).

### Fórmula
$$Fitness = CP - (DT \cdot  \gamma) - \sum P_i$$

### Componentes:
1. **Cobertura Ponderada ($CP$):** Soma da população de todos os bairros que possuem pelo menos um posto com ambulância alocada no turno. Aplicamos pesos de criticidade: 
- Manhã (1.0);
- Tarde (1.2);
- Noite (1.5).
2. **Déficit Total ($DT$):** Calculado em `calcular_deficit`, representa a diferença entre a demanda de ocorrências do bairro e a capacidade de atendimento das ambulâncias alocadas.
3.  **Fator Gamma ($\gamma$):** Um multiplicador de peso ($150$) aplicado ao déficit para garantir que a falta de atendimento impacte severamente o fitness.
4. **Penalidades ($\sum p_i$):**
    * **Restrições Absolutas (Peso 100.000):** R1 (Frota de 15), R2 (Mínimo 1 por posto) e R4 (Bairro sem nenhuma cobertura).
    * **Restrições de Qualidade (Peso 2.000 a 20.000):** R3 (Máximo 4 por posto), R5 (Alta demanda), R6 (Rodízio de equipes) e R7 (Reforço noturno nos postos P4, P5 e P7).

## 3. Operadores

### Seleção
* **Torneio (k=3):** Garante que indivíduos com melhor fitness tenham maior probabilidade de reprodução, mantendo a diversidade genética necessária para evitar convergência prematura.

### Crossover
* **Uniforme por Turno (Colunas):** O operador sorteia colunas inteiras (turnos) entre os pais. 
* **Justificativa Técnica:** Como a restrição **R1** exige que a soma das ambulâncias no turno seja exatamente 15, trocar colunas inteiras entre pais já válidos garante que os filhos mantenham a integridade da frota total sem necessidade de reparação extra.

### Mutação
* **Transferência de Ambulância:** Seleciona-se um turno aleatório, um posto doador e um posto receptor.
* **Tratamento de Restrições:** O doador deve ter no mínimo 1 ambulância (**R2**).
    * O receptor deve ter no máximo 4 ambulâncias (**R3**).
    * A soma total permanece 15 (**R1**).

## 4. Inicialização

* **Estratégia:** Alocação Incremental Aleatória.
* **Garantia de Validade:** O sistema inicia cada turno alocando 1 ambulância por posto. As 7 ambulâncias restantes são distribuídas sorteando postos aleatórios até que o limite de 4 seja atingido ou a frota de 15 se esgote. Isso garante que 100% da população inicial seja viável perante as restrições R1, R2 e R3.

## 5. Critério de Parada e Elitismo

* **Parada:** O algoritmo encerra após um número fixo de gerações (padrão 200), permitindo a observação da curva de convergência.
* **Elitismo:** Os 2 melhores indivíduos de cada geração são preservados integralmente. Isso impede a perda de soluções ótimas encontradas acidentalmente durante processos de mutação agressiva.