import csv
import sys
import os
import seaborn as sns; sns.set()
import numpy as np
from matplotlib import pyplot as plt

filename = sys.argv[1]
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
    plt.ylim([-.05, 1.05])
    plt.yticks(np.arange(0, 1, 0.1))
    plt.legend()
    
    plt.savefig(f"analysis/"+".".join(filename.split(".")[:-1])+".png",
            format="png", bbox_inches="tight") 
    plt.cla(); plt.clf()
