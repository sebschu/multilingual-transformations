import csv
import os
import seaborn as sns; sns.set()
import numpy as np
from matplotlib import pyplot as plt

for filename in os.listdir("."):
    if not filename.startswith("mbart"):
        continue
    aux = "have" if "have" in filename else "do"
    fold = "dev" if "dev" in filename else "gen"
    x = []
    exact = []
    first = []
    with open(filename, "r") as in_file:
        csv_reader = csv.reader(in_file)
        next(csv_reader)   # skip header
        for row in csv_reader:
            iteration, exact_match, first_token = row
            x.append(int(iteration))
            exact.append(float(exact_match))
            first.append(float(first_token))
        new_x, new_exact = zip(*sorted(zip(x, exact)))
        _, new_first = zip(*sorted(zip(x, first)))
        
        sns.set_style("whitegrid")
        plt.plot(new_x, new_exact, label="Exact match")
        plt.plot(new_x, new_first, label="First token")
        plt.xlabel("Iteration")
        plt.ylabel("Accuracy")
        plt.xlim([0, 75000])
        plt.ylim([0, 1])
        plt.yticks(np.arange(0, 1, 0.1))
        plt.legend()
        
        plt.title(f"mBART {fold} \"{aux}\" accuracies (bs=32)")
        plt.savefig(f"analysis/mBART-{aux}-{fold}.png", format="png", bbox_inches="tight") 
        plt.cla(); plt.clf()
