import copy
import argparse
from gerador import gerar_populacao
from selecao import selecionar_por_pais
from crossover import crossover_uniforme
from mutacao import mutacao
from fitness import calcular_fitness

def executar(pop_size, geracoes, crossover_rate, mutacao_rate):
    # Inicializa a população com o tamanho definido via argumento
    populacao = gerar_populacao(pop_size)
    
    print("Iniciando otimização de alocação de ambulâncias...")
    print(f"População: {pop_size} | Gerações: {geracoes}")
    print(f"Taxa Crossover: {crossover_rate} | Taxa Mutação: {mutacao_rate}\n")
    
    for geracao in range(geracoes):
        populacao.sort(key=lambda ind: ind['fitness'], reverse=True)
        
        melhor_geracao = populacao[0]
        
        fitnesses = [ind["fitness"] for ind in populacao]
        print(f"Geração {geracao:3d} | Mínimo: {min(fitnesses):.2f} | Média: {sum(fitnesses)/len(fitnesses):.2f} | Máximo: {melhor_geracao['fitness']:.2f} | Violações: {melhor_geracao['detalhes']['violacoes']}\n")

        nova_populacao = []
        
        # elitismo: mantém os 2 melhores
        nova_populacao.extend(copy.deepcopy(populacao[:2]))
        
        while len(nova_populacao) < pop_size:
            # seleção
            pai1, pai2 = selecionar_por_pais(populacao)
            # crossover
            filho1, filho2 = crossover_uniforme(pai1, pai2, crossover_rate)
            # mutação
            filho1 = mutacao(filho1, mutacao_rate)
            filho2 = mutacao(filho2, mutacao_rate)
            
            for filho in [filho1, filho2]:
                if len(nova_populacao) < pop_size:
                    if 'fitness' not in filho: 
                        dados = calcular_fitness(filho['cromossomo'])
                        filho['fitness'] = dados['fitness']
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
    parser = argparse.ArgumentParser(description="Algoritmo Genético para Alocação de Ambulâncias")

    # Configuração dos argumentos
    parser.add_argument("-p", "--populacao", type=int, default=100, help="Tamanho da população (padrão: 100)")
    parser.add_argument("-g", "--geracoes", type=int, default=100, help="Número de gerações (padrão: 100)")
    parser.add_argument("-c", "--crossover", type=float, default=0.8, help="Taxa de crossover entre 0 e 1 (padrão: 0.8)")
    parser.add_argument("-m", "--mutacao", type=float, default=0.1, help="Taxa de mutação entre 0 e 1 (padrão: 0.1)")

    args = parser.parse_args()

    # chama a função principal com os valores definidos no terminal
    executar(
        pop_size=args.populacao, 
        geracoes=args.geracoes, 
        crossover_rate=args.crossover, 
        mutacao_rate=args.mutacao
    )
    
    