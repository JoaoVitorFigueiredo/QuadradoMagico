import csv

from GeneticAlgorithm import GeneticAlgorithm

order    = int(input("Ordem n do quadrado mágico (n×n, n>=3): "))
if order < 3:
    raise ValueError("n must be >=3 for a magic square.")
pop_size = int(input("Tamanho da população: "))
selector = int(input("Selecione seleção (1: Elitismo, 2: Torneio, 3: Roleta, 4: Torneio + Elitismo, 5: Roleta + Torneio): "))
crossover_rate = float(input("Taxa de crossover [0-1]: "))
mutation_rate  = float(input("Taxa de mutação [0-1]: "))

use_es = input("Usar early stopping? (s/n): ").strip().lower() == 's'
patience = int(input("Paciencia (gerações sem melhora): "))
max_gens = None


print(f"Params: Pop size: {pop_size}; Selector: {selector}; Cross-rate: {crossover_rate}; Mutation-rate: {mutation_rate}")
with open("test_results.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(
        ["pop_size", "selector", "mutation_rate", "crossover_rate", "convergence", "best_fitness"])  # Cabeçalhos

for _ in range(10):
    ga = GeneticAlgorithm(
        n_individuals=pop_size,
        order=order,
        max_generations=max_gens,
        crossover_rate=crossover_rate,
        mutation_rate=mutation_rate,
        selector=selector,
        early_stopping=True,
        patience=patience
    )

    result = ga.start()

    with open("test_results.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [pop_size, selector, mutation_rate, crossover_rate, ga.convergence, result.get_fitness()])
