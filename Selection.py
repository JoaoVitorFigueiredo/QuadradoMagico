import random


class Selection:
    def __init__(self, n_selected: int, threshold: float = 0):
        # criar uma verificação se n_selected é um inteiro entre 2 e o número da população e
        self.n_selected = n_selected
        self.threshold = threshold

    def apply_selection(self, candidates: list):
        pass

    # Não sei se isso é algo bacana pra se usar mas fica aqui, dá pra replicar nas restantes funções debaixo
    def apply_threshold(self, candidates: list):
        for candidate in candidates:
            if candidate.get_fitness() < self.threshold:
                candidates.remove(candidate)
        return candidates


class TournamentSelection (Selection):
    def __init__(self, n_selected, threshold=0):
        super().__init__(n_selected, threshold)

    # AINDA PRECISA DE TESTES
    def apply_selection(self, candidates: list):
        if len(candidates) > self.n_selected:
            winners = []
            while len(candidates) > 0:
                candidate_1 = random.choice(candidates)
                candidates.remove(candidate_1)

                candidate_2 = random.choice(candidates)
                candidates.remove(candidate_2)

                if candidate_1.get_fitness > candidate_2.get_fitness:
                    winners.append(candidate_1)

                else:
                    winners.append(candidate_2)

            return self.apply_selection(winners)

        return candidates


class Elitism (Selection):
    def __init__(self, n_selected, threshold=0):
        super().__init__(n_selected, threshold)

    def apply_selection(self, candidates: list):
        candidates.sort()
        candidates = candidates[:self.n_selected+1]
        return candidates


class WheelSelection (Selection):
    def __init__(self, n_selected, threshold=0):
        super().__init__(n_selected, threshold)

    def apply_selection(self, candidates: list):
        selected = []
        while len(selected) < self.n_selected:
            total = sum(candidates)
            current_pos = 0
            chosen_pos = random.uniform(0, total)

            for candidate in candidates:
                current_pos += candidate.get_fitness()/total
                if chosen_pos <= current_pos:
                    selected.append(candidate)
                    candidates.remove(candidate)
                    break

        return selected







