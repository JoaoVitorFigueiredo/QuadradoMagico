import csv
import os
import matplotlib.pyplot as plt
from GeneticAlgorithm import GeneticAlgorithm

# -----------------------------------------------------------------------------
# 1) Define your experiments
# -----------------------------------------------------------------------------
# Each dict here is one full test: pop_size, mutation_rate, selector, patience
experiments = [
    {"pop_size": 200, "mutation_rate": 0.01, "selector": 4, "patience": 500},
    {"pop_size": 200, "mutation_rate": 0.05, "selector": 4, "patience": 500},
    {"pop_size": 200, "mutation_rate": 0.1, "selector": 4, "patience": 500},
    {"pop_size": 200, "mutation_rate": 0.2, "selector": 4, "patience": 500},
    # add more here...
]

order = 10   # fixed for all experiments; change as needed
runs_per_experiment = 10

# -----------------------------------------------------------------------------
# 2) Helper to build a short tag from params
# -----------------------------------------------------------------------------
sel_map = {1: "E", 2: "T", 3: "R", 4: "T+E", 5: "R+T"}

def make_tag(cfg):
    ps = cfg["pop_size"]
    mu = cfg["mutation_rate"]
    sl = sel_map.get(cfg["selector"], f"?{cfg['selector']}")
    pt = cfg["patience"]
    return f"P{ps}_M{int(mu*100)}_S{sl}_Pat{pt}"

# -----------------------------------------------------------------------------
# 3) Run each experiment
# -----------------------------------------------------------------------------
for cfg in experiments:
    tag = make_tag(cfg)
    csv_file = f"results_{tag}.csv"
    img_file = f"envelope_{tag}.png"
    
    # Prepare CSV
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["run", "gens_ran", "final_best_fitness"])
    
    # Collect curves
    all_curves = []
    for run in range(1, runs_per_experiment+1):
        ga = GeneticAlgorithm(
            n_individuals   = cfg["pop_size"],
            order           = order,
            max_generations = None,                # always early‐stop
            mutation_rate   = cfg["mutation_rate"],
            selector        = cfg["selector"],
            early_stopping  = True,
            patience        = cfg["patience"]
        )
        best = ga.start()
        curve = ga.best_fitness
        all_curves.append(curve)
        
        gen_solve = len(curve)
        final_fit = best.get_fitness()
        
        # Append to CSV
        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([run, gen_solve, final_fit])
    
    # Pad curves to same length for envelope
    max_len = max(len(c) for c in all_curves)
    padded = [c + [c[-1]]*(max_len-len(c)) for c in all_curves]
    
    best_curve  = [max(curve[i] for curve in padded) for i in range(max_len)]
    avg_curve   = [sum(curve[i] for curve in padded)/len(padded) for i in range(max_len)]
    worst_curve = [min(curve[i] for curve in padded) for i in range(max_len)]
    gens = list(range(1, max_len+1))
    
    # Plot envelope
    plt.figure(figsize=(8,5))
    plt.plot(gens, best_curve,  label="Best-of-10",   linewidth=2)
    plt.plot(gens, avg_curve,   label="Average-of-10", linestyle="--")
    plt.plot(gens, worst_curve, label="Worst-of-10",   linestyle=":")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.title(f"GA Envelope ({tag})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(img_file)
    plt.close()
    
    print(f"Experiment {tag} done → {csv_file}, {img_file}")
