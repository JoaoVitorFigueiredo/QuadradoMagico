from __future__ import annotations

from statistics import mean

import random

import Individual


class Utils:
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

        return Individual.Individual(new_individual_cube)

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

        return Individual.Individual(new_individual_cube)


if __name__ == "__main__":

    pass