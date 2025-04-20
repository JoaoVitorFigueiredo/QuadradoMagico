import random

class Selection:
    def __init__(self, n_selected: int, threshold: float = float('-inf')):
        assert n_selected >= 1
        self.n_selected = n_selected
        self.threshold  = threshold

    def apply_threshold(self, pop):
        return [ind for ind in pop if ind.get_fitness() >= self.threshold]

    def apply_selection(self, pop):
        return self.apply_threshold(pop)[:self.n_selected]


class TournamentSelection(Selection):
    def __init__(self, n_selected: int, threshold: float = float('-inf'), tour_size: int = 2):
        super().__init__(n_selected, threshold)
        assert tour_size >= 2
        self.tour_size = tour_size

    def apply_selection(self, pop):
        pool = self.apply_threshold(pop)
        selected = []
        while len(selected) < self.n_selected:
            tour = random.sample(pool, min(self.tour_size, len(pool)))
            winner = max(tour, key=lambda ind: ind.get_fitness())
            selected.append(winner)
        return selected


class Elitism(Selection):
    def apply_selection(self, pop):
        pool = self.apply_threshold(pop)
        sorted_pop = sorted(pool, key=lambda ind: ind.get_fitness(), reverse=True)
        return sorted_pop[:self.n_selected]


class WheelSelection(Selection):
    def apply_selection(self, pop):
        pool = self.apply_threshold(pop)
        fits = [ind.get_fitness() for ind in pool]
        minf = min(fits)
        weights = [(f - minf + 1e-6) for f in fits]
        total   = sum(weights)

        selected = []
        while len(selected) < self.n_selected:
            r = random.uniform(0, total)
            cum = 0
            for ind, w in zip(pool, weights):
                cum += w
                if r <= cum:
                    selected.append(ind)
                    break
        return selected
