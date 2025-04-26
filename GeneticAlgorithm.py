import random
import copy
from Individual import Individual, IndividualUtils
from Selection import TournamentSelection, Elitism, WheelSelection, HybridSelection, MixedSelection

import matplotlib.pyplot as plt

import time

import csv

class GeneticAlgorithm:
    def __init__(self,
                 n_individuals: int,
                 order: int,
                 max_generations: int = None,
                 mutation_rate: float = 0.2,
                 elitism_count: int = 1,
                 selector: int = 2,
                 early_stopping: bool = False,
                 patience: int = None):
        self.convergence = None

        self.n_individuals   = n_individuals
        self.order           = order
        # max_generations is None when using early stopping only
        self.max_generations = max_generations
        self.mutation_rate   = mutation_rate
        self.elitism_count   = elitism_count
        self.early_stopping  = early_stopping
        self.patience        = patience
        self.chromosome_len  = order * order
        self.population      = []

        # Number of parents based on population
        self.n_parents = max(2, self.n_individuals // 20)
        # Select selection strategy
        if selector == 1:
            self.selector = Elitism(self.n_parents)
        elif selector == 2:
            self.selector = TournamentSelection(self.n_parents)
        elif selector == 3:
            self.selector = WheelSelection(self.n_parents)
        elif selector == 4:
            self.selector = HybridSelection(self.n_parents)
        elif selector == 5:
            self.selector = MixedSelection(self.n_parents)
        else:
            self.selector = TournamentSelection(self.n_parents)

        # Tracking for plotting
        self.best_fitness = []
        self.avg_fitness  = []

    def mean_fitness(self):
        return sum(ind.get_fitness() for ind in self.population) / len(self.population)

    def start(self):
        self._init_population()
        best_so_far = float('-inf')
        no_improve = 0
        gen = 0

        while True:
            gen += 1
            # Record fitness
            best = max(self.population, key=lambda ind: ind.get_fitness())
            current_best = best.get_fitness()
            self.best_fitness.append(current_best)
            self.avg_fitness.append(self.mean_fitness())

            # Early stopping logic
            if self.early_stopping:
                if current_best > best_so_far:
                    best_so_far = current_best
                    no_improve = 0
                else:
                    no_improve += 1
                if no_improve >= self.patience:
                    print(f"Early stopping at generation {gen} after {self.patience} gens without improvement.")
                    self.convergence = self.patience - gen
                    break

            # Max generation stopping
            if not self.early_stopping:
                if gen >= self.max_generations:
                    print(f"Reached max generations: {self.max_generations}.")
                    break

            # Check perfect solution
            if current_best == 0:
                print(f"SOLVED at generation {gen}")
                self.convergence = gen
                print(best)
                break

            # Produce next gen
            parents = self.selector.apply_selection(self.population)
            next_pop = Elitism(self.elitism_count).apply_selection(self.population)
            while len(next_pop) < self.n_individuals:
                p1, p2 = random.sample(parents, 2)
                child = IndividualUtils.crossover_one_point(p1, p2)
                if random.random() < self.mutation_rate:
                    child.mutation()
                next_pop.append(child)
            self.population = next_pop

        # End: print best
        best = max(self.population, key=lambda ind: ind.get_fitness())
        print("Best found:")
        print(best)
        print("Fitness:", best.get_fitness())
        return best

    def _init_population(self):
        self.population = []
        for _ in range(self.n_individuals):
            cube = random.sample(range(1, self.chromosome_len + 1), self.chromosome_len)
            self.population.append(Individual(cube, order=self.order))

if __name__ == "__main__":
    order    = int(input("Ordem n do quadrado mágico (n×n, n>=3): "))
    if order < 3:
        raise ValueError("n must be >=3 for a magic square.")
    pop_size = int(input("Tamanho da população: "))
    selector = int(input("Selecione seleção (1: Elitismo, 2: Torneio, 3: Roleta, 4: Torneio + Elitismo, 5: Roleta + Torneio): "))
    mutation_rate  = float(input("Taxa de mutação [0-1]: "))

    use_es = input("Usar early stopping? (s/n): ").strip().lower() == 's'
    if use_es:
        patience = int(input("Paciencia (gerações sem melhora): "))
        max_gens = None
    else:
        patience = None
        max_gens = int(input("Máximo de gerações: "))

    print(f"Params: Pop size: {pop_size}; Selector: {selector}; Mutation-rate: {mutation_rate}")

    ga = GeneticAlgorithm(
        n_individuals=pop_size,
        order=order,
        max_generations=max_gens,
        mutation_rate=mutation_rate,
        selector=selector,
        early_stopping=use_es,
        patience=patience
    )

    start_time = time.perf_counter()
    ga.start()
    end_time = time.perf_counter()

    print(f"Execution time: {end_time - start_time}")

    # Plot
    gens = list(range(1, len(ga.best_fitness)+1))
    plt.plot(gens, ga.best_fitness, label='Best')
    plt.plot(gens, ga.avg_fitness,  label='Average')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('GA Convergence')
    plt.legend()
    plt.grid()
    plt.savefig("graph.png")

    plt.ylim(-200, 0)

    plt.savefig("graph-ylimit.png")

    #para fazer gráficos melhores mais fácil
    with open("fitness_results.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["geração", "melhor", "média"])  # Cabeçalhos

        for gen, (best, avg) in enumerate(zip(ga.best_fitness, ga.avg_fitness), start=1):
            writer.writerow([gen, best, avg])


    with open("test_results.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["pop_size", "selector", "convergence", "best_fitness", "mutation_rate", "crossover_rate"])  # Cabeçalhos


        writer.writerow([gen, best, avg])
