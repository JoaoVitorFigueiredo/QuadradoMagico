import random

from Utils import Utils


class Individual:
    def __init__(self, cube: list):
        self.__cube = cube
        self.__loss = Utils.fitness_function(cube)

    def get_cube(self):
        return self.__cube

    def mutation(self):
        idx = range(len(self.__cube))
        i1, i2 = random.sample(idx, 2)
        self.__cube[i1], self.__cube[i2] = self.__cube[i2], self.__cube[i1]

    def __str__(self):
        return self.__cube.__str__()


if __name__ == "__main__":
    individual = Individual([1, 2, 3, 4, 5, 6, 7, 8, 9])
    individual.mutation()
    print(individual)
    individual.mutation()
    print(individual)
    individual.mutation()
    print(individual)


