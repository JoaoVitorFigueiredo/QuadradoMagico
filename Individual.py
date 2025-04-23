import random


class Individual:
    def __init__(self, cube: list, order: int = 3):
        """
        :param cube: flat list of length order*order representing the square
        :param order: dimension n of the square (n×n)
        """
        assert len(cube) == order * order, f"Expected {order * order} values, got {len(cube)}"
        assert len(cube) == len(set(cube))  # check for duplicates
        self.order = order
        self._cube = cube[:]  # copy
        self._fitness = IndividualUtils.fitness_function(self)

    def get_cube(self):
        return self._cube[:]

    def set_cube(self, new_cube: list):
        assert len(new_cube) == self.order * self.order
        self._cube = new_cube[:]
        self._fitness = IndividualUtils.fitness_function(self)

    def get_fitness(self):
        return self._fitness

    def mutation(self):
        # swap two genes and recompute fitness
        i1, i2 = random.sample(range(self.order * self.order), 2)
        self._cube[i1], self._cube[i2] = self._cube[i2], self._cube[i1]
        self._fitness = IndividualUtils.fitness_function(self)

    def __str__(self):
        # pretty-print rows
        rows = [self._cube[i * self.order:(i + 1) * self.order] for i in range(self.order)]
        return "\n".join(str(r) for r in rows)

    def __gt__(self, other):
        return self.get_fitness() > other.get_fitness()

    def __lt__(self, other):
        return self.get_fitness() < other.get_fitness()

    @staticmethod
    def new_cube(order: int = 3):
        new_cube = []
        for _ in range(order * order):
            new_number = random.randint(1, 9)
            if new_number not in new_cube:
                new_cube.append(new_number)
        return Individual(new_cube, order)


class IndividualUtils:
    @staticmethod
    def fitness_function(ind: Individual):
        """
        Fitness = -sum( | sum(row / col / diag) - magic |), where
        magic = n * (n ^ 2 + 1) / 2
        Perfect
        square = > fitness = 0
        :param ind:
        :return:
        """
        n = ind.order
        cube = ind.get_cube()
        # build n×n matrix
        grid = [cube[i * n:(i + 1) * n] for i in range(n)]
        magic = n * (n * n + 1) // 2

        errors = []
        # rows & cols
        for i in range(n):
            errors.append(abs(sum(grid[i]) - magic))
            errors.append(abs(sum(grid[r][i] for r in range(n)) - magic))

        # diags
        errors.append(abs(sum(grid[i][i] for i in range(n)) - magic))
        errors.append(abs(sum(grid[i][n - 1 - i] for i in range(n)) - magic))

        loss = sum(errors)
        return -loss

    @staticmethod
    def crossover_one_point(ind1: Individual, ind2: Individual):
        n2 = ind1.order * ind1.order
        p = random.randint(1, n2 - 1)
        head = ind1.get_cube()[:p]
        tail = [x for x in ind2.get_cube() if x not in head]
        return Individual(head + tail, order=ind1.order)

    @staticmethod
    def crossover_two_point(ind1: Individual, ind2: Individual):
        n2 = ind1.order * ind1.order
        p1 = random.randint(0, n2 - 2)
        p2 = random.randint(p1 + 1, n2 - 1)
        slice_ = ind1.get_cube()[p1:p2]
        rest = [x for x in ind2.get_cube() if x not in slice_]
        child = rest[:p1] + slice_ + rest[p1:]
        return Individual(child, order=ind1.order)




if __name__ == "__main__":
    ind = Individual([1, 2, 3, 4, 5, 6, 7, 8, 9])
