import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.stats import linregress
import numpy as np


# Initialize an empty list to store the extracted data
data = []

# Open the text file for reading
with open("results/results_best-imp.exp1.txt", "r") as file:
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
    if entry[4] not in sudoku_stats:
        sudoku_stats[entry[4]] = {}

    if entry[5] not in sudoku_stats[entry[4]]:
        sudoku_stats[entry[4]][entry[5]] = {}

    sudoku_stats[entry[4]][entry[5]][entry[0]] = entry[8]

for sudoku, tries in sudoku_stats.items():
    normalized_stats = {}
    stats = {}
    for try_n, stat in tries.items():
        all_values = [values for stat in tries.values() for values in stat.values()]
        #/max(all_values)
        values = zip(stat.keys(), [switches for oc, switches in stat.items()])
        for oc, n_switches in values:
            if oc not in stats:
                stats[oc] = []

            stats[oc].append(n_switches)

    average_stats = {}
    for oc, values in stats.items():
        average_switches_per_sudoku[oc].append(sum(values) / len(values))

# Calculating the average for each (optimization credit, sudoku) pair
for key in average_switches_per_sudoku:
    average_switches_per_sudoku[key] = sum(average_switches_per_sudoku[key]) / len(average_switches_per_sudoku[key])

# Preparing data for plotting
# x_values = [key[0] for key in average_switches_per_sudoku.keys()]  # Optimization credits
# y_values = list(average_switches_per_sudoku.values())             # Averaged number of switches

# 1 -> 32
# 2 -> 30
# 3 -> 28
# 4 -> 30
# 5 -> 36

# Creating the scatter plot
plt.figure(figsize=(12, 8))

# # Assign a unique color to each Sudoku
# colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'orange', 'purple', 'brown']
# color_index = 0
#
# for sudoku in set(key[1] for key in average_switches_per_sudoku.keys()):
#     # Filter the data for the current Sudoku
#     x_values = [key[0] for key in average_switches_per_sudoku.keys() if key[1] == sudoku]
#     y_values = [average_switches_per_sudoku[key] for key in average_switches_per_sudoku.keys() if key[1] == sudoku]
#
#     # Plot the data for the current Sudoku
#     plt.scatter(x_values, y_values, color=colors[color_index], label=f'Sudoku {sudoku}')
#     color_index = (color_index + 1) % len(colors)

x_values = [key for key in average_switches_per_sudoku.keys()]
y_values = [average_switches_per_sudoku[key] for key in average_switches_per_sudoku.keys()]

plt.scatter(x_values, y_values, color='blue')

# Fit a line (polynomial fit)
# Perform linear regression
slope, intercept, _, _, _ = linregress(x_values, y_values)

# Calculate the best-fit line
best_fit = slope * np.array(x_values) + intercept

# Plot the best-fit line
plt.plot(x_values, best_fit, color='red', label='Best Fit Line (Linear Regression)')

plt.xticks(np.arange(min(x_values), max(x_values)+1, step=1))

plt.annotate(y_values[3], (4, y_values[3]), xytext=(0, 15), textcoords='offset points', ha='center', va='bottom', fontsize=8,
                 bbox=dict(boxstyle='round,pad=1', fc='white', alpha=0.8))

# plt.annotate(y_values[13], (14, y_values[13]), xytext=(0, 15), textcoords='offset points', ha='center', va='bottom', fontsize=8,
#                  bbox=dict(boxstyle='round,pad=1', fc='white', alpha=0.8))

plt.title('Best improvement: Average normalized #switches vs. Optimization credits (for all Sudoku)')
plt.xlabel('Optimization credits')
plt.ylabel('Average normalized #switches')
plt.grid(True)
plt.show()
