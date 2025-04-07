import random
from statistics import mean


class Individual:
    def __init__(self, cube: list):
        self.__cube = cube
        self.__fitness = IndividualUtils.fitness_function(cube)

    def get_cube(self):
        return self.__cube

    def get_fitness(self):
        return self.__fitness

    def mutation(self):
        idx = range(len(self.__cube))
        i1, i2 = random.sample(idx, 2)
        self.__cube[i1], self.__cube[i2] = self.__cube[i2], self.__cube[i1]

    def __str__(self):
        return self.__cube.__str__()


class IndividualUtils:
    @staticmethod
    def fitness_function(cube: list):
        """

        :param cube:

        [0,1,2,
        3,4,5
        6,7,8]

        0+3+6 = 1+4+7 = 2+5+8 = 0+1+2 = 3+4+5 = 6+7+8


        :return:
        """
        results = [cube[0]+cube[3]+cube[6],
                   cube[1]+cube[4]+cube[7],
                   cube[2]+cube[5]+cube[6],
                   cube[0]+cube[1]+cube[3],
                   cube[3]+cube[4]+cube[5],
                   cube[6]+cube[7]+cube[8]]

        mean_sum = mean(results)

        loss = 0

        for result in results:
            if (result-mean_sum) > 0:
                loss += result-mean_sum
            else:
                loss -= result-mean_sum
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
    def crossover_two_point(ind1: "Individual", ind2: "Individual"):
        crossover_point_1 = random.randint(1, 6)
        crossover_point_2 = random.randint(crossover_point_1+2,9)

        new_individual_cube = []

        for i in range(crossover_point_1):
            new_individual_cube.append(ind1.get_cube()[i])
        for i in range(crossover_point_1, crossover_point_2):
            new_individual_cube.append(ind2.get_cube()[i])
        for i in range(crossover_point_2,9):
            new_individual_cube.append(ind1.get_cube()[i])

        return Individual(new_individual_cube)


if __name__ == "__main__":
    cubo_teste_2 = [2, 4, 6, 8, 10, 12, 14, 16, 18]
    cubo_teste_1 = [1, 3, 5, 7, 9, 11, 13, 15, 17]

    ind_1 = Individual(cubo_teste_1)
    ind_2 = Individual(cubo_teste_2)

    print(IndividualUtils.crossover_one_point(ind_1, ind_2))

    pass


