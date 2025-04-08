import random

from Individual import Individual


class GeneticAlgorithm:

    def __init__(self, n_individuals: int):
        self.__n_individuals = n_individuals
        self.__population = []

    def start(self):
        """
        This function will start the Genetic Algorithm
        :return:
        """
        pass

    def __generate_first_population(self):
        for _ in range(self.__n_individuals):
            new_cube = []
            for _ in range(8):
                new_cube.append(random.randint(0, 9))
            self.__population.append(Individual(new_cube))


if __name__ == "__main__":
    # Inputs do utilizado
    n_individuals = int(input("Insira o tamanho da população: "))

    # Inicialização do algoritmo
    alg = GeneticAlgorithm(n_individuals=n_individuals)

    # Execução do algoritmo
    alg.start()
