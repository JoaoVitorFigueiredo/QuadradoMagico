import random
from statistics import mean


class Individual:
    def __init__(self, cube: list):
        self.__cube = cube
        self.__fitness = IndividualUtils.fitness_function(self)

    def get_cube(self):
        return self.__cube

    def set_cube(self, new_cube=list):
        self.__cube = new_cube

    def get_fitness(self):
        return self.__fitness

    def mutation(self):
        idx = range(len(self.__cube))
        i1, i2 = random.sample(idx, 2)
        self.__cube[i1], self.__cube[i2] = self.__cube[i2], self.__cube[i1]

    def __str__(self):
        return self.__cube.__str__()

    def __gt__(self, other):
        return self.get_cube() >= other.get_cube()

    def __int__(self):
        return self.get_cube()


class IndividualUtils:
    @staticmethod
    def fitness_function(ind: Individual):
        """

        :param ind:

        [0,1,2,
        3,4,5
        6,7,8]

        0+3+6 = 1+4+7 = 2+5+8 = 0+1+2 = 3+4+5 = 6+7+8


        :return:
        """
        cube = ind.get_cube()

        results = [cube[0] + cube[3] + cube[6],
                   cube[1] + cube[4] + cube[7],
                   cube[2] + cube[5] + cube[8],
                   cube[0] + cube[1] + cube[2],
                   cube[3] + cube[4] + cube[5],
                   cube[6] + cube[7] + cube[8]]

        mean_sum = mean(results)

        loss = 0

        for result in results:
            if (result - mean_sum) < 0:
                loss += result - mean_sum
            else:
                loss -= result - mean_sum
        return loss

    @staticmethod
    def crossover_one_point(ind1: "Individual", ind2: "Individual"):
        crossover_point = random.randint(1, 8)
        new_individual_cube = []
        for i in range(crossover_point):
            new_individual_cube.append(ind1.get_cube()[i])
        for i in range(crossover_point, 9):
            new_individual_cube.append(ind2.get_cube()[i])

        return Individual(new_individual_cube)

    @staticmethod
    def crossover_two_point(ind1: Individual, ind2: Individual):
        crossover_point_1 = random.randint(1, 6)
        crossover_point_2 = random.randint(crossover_point_1 + 2, 9)

        new_individual_cube = []

        for i in range(crossover_point_1):
            new_individual_cube.append(ind1.get_cube()[i])
        for i in range(crossover_point_1, crossover_point_2):
            new_individual_cube.append(ind2.get_cube()[i])
        for i in range(crossover_point_2, 9):
            new_individual_cube.append(ind1.get_cube()[i])

        return Individual(new_individual_cube)

    @staticmethod
    def mutation(ind: Individual):
        cube = ind.get_cube()

        gene_1_index = random.randint(0, 8)
        gene_2_index = random.randint(0, 8)

        while gene_1_index == gene_2_index:
            gene_2_index = random.randint(0, 8)

        cube[gene_1_index], cube[gene_2_index] = cube[gene_2_index], cube[gene_1_index]

        ind.set_cube(cube)


if __name__ == "__main__":
    cubo_teste_2 = [2, 2, 9, 3, 9, 9, 2, 2, 4]
    cubo_teste_1 = [1, 3, 5, 7, 9, 11, 13, 15, 17]

    ind_1 = Individual(cubo_teste_1)
    ind_2 = Individual(cubo_teste_2)

    print(ind_2.get_fitness())

    print(IndividualUtils.crossover_one_point(ind_1, ind_2))

    pass
