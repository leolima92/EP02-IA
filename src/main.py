import copy
from problema import TAMANHO_POPULACAO, GERACOES, TAXA_CROSSOVER, TAXA_MUTACAO
from gerador import gerar_populacao
from selecao import selecionar_por_pais
from crossover import crossover_uniforme
from mutacao import mutacao
from fitness import calcular_fitness

def executar():
    populacao = gerar_populacao(TAMANHO_POPULACAO)
    
    print("Iniciando otimização de alocação de ambulâncias...")
    print(f"População: {TAMANHO_POPULACAO} | Gerações: {GERACOES}\n")
    
    for geracao in range(GERACOES):
        populacao.sort(key=lambda ind: ind['fitness'], reverse=True)
        
        melhor_geracao = populacao[0]
        
        if geracao % 20 ==0:
            print(f"Geração {geracao:3d} | Melhor Fitness: {melhor_geracao['fitness']:10.2f} | Violações: {melhor_geracao['detalhes']['violacoes']}")
        
        nova_populacao = []
        
        nova_populacao.extend(copy.deepcopy(populacao[:2]))
        
        while len(nova_populacao) < TAMANHO_POPULACAO:
            #Seleção por torneio
            pai1, pai2 = selecionar_por_pais(populacao)
            #Crossover
            filho1, filho2 = crossover_uniforme(pai1, pai2, TAXA_CROSSOVER)
            #Mutação
            filho1 = mutacao(filho1, TAXA_MUTACAO)
            filho2 = mutacao(filho2, TAXA_MUTACAO)
            
            for filho in [filho1, filho2]:
                if len(nova_populacao) < TAMANHO_POPULACAO:
                    dados = calcular_fitness(filho['cromossomo'])
                    filho
                    filho['detalhes'] = dados
                nova_populacao.append(filho)
        populacao = nova_populacao
        
    populacao.sort(key=lambda ind: ind['fitness'], reverse=True)
    vencedor = populacao[0]
    detalhes = vencedor['detalhes']
    
    print("\nMelhor Solução Encontrada:")
    print("="*50)
    print("Posto | Manhã | Tarde | Noite")
    for i, linha in enumerate(vencedor['cromossomo']):
        print(f" P{i+1}   |   {linha[0]}   |   {linha[1]}   |   {linha[2]}")
    
    print("-" * 50)
    print(f"Fitness Final: {vencedor['fitness']:.2f}")
    print(f"Déficit Total de Ocorrências: {detalhes['deficit_total']}")
    print(f"Violações de Restrições: {detalhes['violacoes']}")
    
    for turno, info in detalhes['cobertura_por_turno'].items():
        print(f"Cobertura {turno:5s}: {info['percentual']:.1f}% da população")

if __name__ == "__main__":
    executar()