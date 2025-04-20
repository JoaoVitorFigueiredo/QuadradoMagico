import random
import copy
from Individual import Individual, IndividualUtils
from Selection import TournamentSelection, Elitism, WheelSelection

class GeneticAlgorithm:
    def __init__(self,
                 n_individuals: int,
                 order: int,
                 max_generations: int = 1000,
                 crossover_rate: float = 0.8,
                 mutation_rate: float = 0.2,
                 elitism_count: int = 1):
        self.n_individuals   = n_individuals
        self.order           = order
        self.chromosome_len  = order * order
        self.max_generations = max_generations
        self.crossover_rate  = crossover_rate
        self.mutation_rate   = mutation_rate
        self.elitism_count   = elitism_count
        self.population      = []

    def start(self):
        """Run GA until a perfect magic square is found or max_generations."""
        self._init_population()

        for gen in range(1, self.max_generations+1):
            # Check for perfect (fitness == 0 loss → fitness = 0)
            best = max(self.population, key=lambda ind: ind.get_fitness())
            if best.get_fitness() == 0:
                print(f"SOLVED at gen {gen-1}")
                print(best)
                return best

            # selection (pick self.n_individuals parents)
            selector = TournamentSelection(self.n_individuals, threshold= -999)
            parents  = selector.apply_selection(self.population)

            # build next generation
            next_pop = []
            # elitism
            elites = Elitism(self.elitism_count).apply_selection(self.population)
            next_pop.extend(elites)

            while len(next_pop) < self.n_individuals:
                # crossover
                if random.random() < self.crossover_rate:
                    p1, p2 = random.sample(parents, 2)
                    child = IndividualUtils.crossover_one_point(p1, p2)
                else:
                    child = copy.deepcopy(random.choice(parents))

                # mutation
                if random.random() < self.mutation_rate:
                    child.mutation()

                next_pop.append(child)

            self.population = next_pop

        # if we exit loop, no perfect found
        best = max(self.population, key=lambda ind: ind.get_fitness())
        print(f"NO perfect in {self.max_generations} gens.")
        print("Best found:\n", best, "\nfitness:", best.get_fitness())
        return best

    def _init_population(self):
        self.population = []
        for _ in range(self.n_individuals):
            # random permutation of 1…n²
            cube = random.sample(range(1, self.chromosome_len+1), self.chromosome_len)
            self.population.append(Individual(cube, order=self.order))


if __name__ == "__main__":
    order         = int(input("Insira a ordem n do quadrado mágico (n×n): "))
    pop_size      = int(input("Insira o tamanho da população: "))
    max_gens      = int(input("Máximo de gerações [e.g. 1000]: "))
    crossover_rate = float(input("Taxa de crossover [0.0–1.0]: "))
    mutation_rate  = float(input("Taxa de mutação [0.0–1.0]: "))

    ga = GeneticAlgorithm(
        n_individuals=pop_size,
        order=order,
        max_generations=max_gens,
        crossover_rate=crossover_rate,
        mutation_rate=mutation_rate
    )
    ga.start()
