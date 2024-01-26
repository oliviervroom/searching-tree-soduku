import math

import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.stats import linregress
import numpy as np

# Initialize an empty list to store the extracted data
data = []
normalize = True

# Open the text file for reading
with open("results/results_cbt.exp2.txt", "r") as file:
    for line in file:
        # Evaluate the line using eval() to get a tuple
        entry_tuple = eval(line.strip())

        # Flatten the tuple and append it to the data
        flattened_entry = []
        for item in entry_tuple:
            if isinstance(item, tuple):
                flattened_entry.extend(item)
            else:
                flattened_entry.append(item)

        data.append(flattened_entry)

# Grouping the data by (optimization credit, sudoku) and averaging the tries
average_switches_per_sudoku = defaultdict(list)
sudoku_stats = {}
for entry in data:
    if entry[2] not in sudoku_stats:
        sudoku_stats[entry[2]] = {}

    if entry[0] not in sudoku_stats[entry[2]]:
        sudoku_stats[entry[2]][entry[0]] = {}

    sudoku_stats[entry[2]][entry[0]][entry[1]] = entry[3]

average_ct = {}
for solver, results in sudoku_stats.items():

    for n_fixed_values, variants in results.items():
        if solver not in average_ct:
            average_ct[solver] = {}

        average_ct[solver][n_fixed_values] = sum(variants.values()) / len(variants)

    if normalize:
        for solver, results in average_ct.items():
            for n_fixed_values, average in results.items():
                average_ct[solver][n_fixed_values] = average / max(average_ct[solver].values())

# Creating the scatter plot
plt.figure(figsize=(12, 8))

average_ct = {k: average_ct[k] for k in sorted(average_ct)}

# Assign a unique color to each Sudoku
colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'orange', 'purple', 'brown']
color_index = 0

plots = []
for solver in average_ct.keys():
    # Filter the data for the current Sudoku
    x_values = list(average_ct[solver].keys())
    y_values = list(average_ct[solver].values())

    # Plot the data for the current Sudoku
    plt.scatter(x_values, y_values, color=colors[color_index], label=f'Solver {solver}')
    plots.append(*plt.plot(x_values, y_values, color=colors[color_index], label=f'Solver {solver}'))

    color_index = (color_index + 1) % len(colors)


# Adding a legend
plt.legend(plots, ['CBT', 'FWC', 'MCV'])
plt.gca().invert_xaxis()

plt.xticks(np.arange(min(x_values), max(x_values)+1, step=1))

# plt.annotate(math.floor(average_ct[2][17]*100)/100, (17, average_ct[2][17]), xytext=(0, 15), textcoords='offset points', ha='center', va='bottom', fontsize=8,
#                  bbox=dict(boxstyle='round,pad=1', fc='white', alpha=0.8))
#
# plt.annotate(math.floor(average_ct[1][19]), (19, average_ct[1][19]), xytext=(0, 15), textcoords='offset points', ha='center', va='bottom', fontsize=8,
#                  bbox=dict(boxstyle='round,pad=1', fc='white', alpha=0.8))
#
# plt.annotate(math.floor(average_ct[0][18]), (18, average_ct[0][18]), xytext=(0, 15), textcoords='offset points', ha='center', va='bottom', fontsize=8,
#                  bbox=dict(boxstyle='round,pad=1', fc='white', alpha=0.8))

plt.title('CBT vs FWC vs MCV: Normalized Computing Time vs. #Fixed Values')
plt.ylabel('Computing Time (normalized)')
plt.xlabel('#Fixed Values')
plt.grid(True)
plt.show()
