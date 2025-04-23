import random

class Selection:
    def __init__(self, n_selected: int, threshold: float = float('-inf')):
        assert n_selected >= 1
        self.n_selected = n_selected
        self.threshold = threshold

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
        total = sum(weights)

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


class HybridSelection(Selection):
    """
    Combines elitism and tournament selection:
    - Keeps top `elite_count` individuals
    - Fills the rest via tournaments of size `tour_size`
    """
    def __init__(self, n_selected: int, elite_count: int = 1, tour_size: int = 2, threshold: float = float('-inf')):
        super().__init__(n_selected, threshold)
        assert elite_count < n_selected, "elite_count must be less than n_selected"
        self.elite_count = elite_count
        self.tourney = TournamentSelection(n_selected - elite_count, threshold, tour_size)

    def apply_selection(self, pop):
        # Step 1: select elites
        elites = Elitism(self.elite_count, self.threshold).apply_selection(pop)
        # Step 2: tournament among remaining
        remaining = [ind for ind in pop if ind not in elites]
        tour_winners = self.tourney.apply_selection(remaining)
        return elites + tour_winners


class MixedSelection(Selection):
    """
    Mixes tournament and roulette selection:
    - Picks pct_tourney fraction via tournament
    - Picks the rest via roulette
    """
    def __init__(self, n_selected: int, pct_tourney: float = 0.5, tour_size: int = 2, threshold: float = float('-inf')):
        super().__init__(n_selected, threshold)
        assert 0 <= pct_tourney <= 1, "pct_tourney must be between 0 and 1"
        self.n_tourney = int(n_selected * pct_tourney)
        self.n_roulette = n_selected - self.n_tourney
        self.tourney = TournamentSelection(self.n_tourney, threshold, tour_size)
        self.roulette = WheelSelection(self.n_roulette, threshold)

    def apply_selection(self, pop):
        tour_sel = self.tourney.apply_selection(pop)
        wheel_sel = self.roulette.apply_selection(pop)
        return tour_sel + wheel_sel