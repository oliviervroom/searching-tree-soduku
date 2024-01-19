import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.stats import linregress
import numpy as np

# Initialize an empty list to store the extracted data
data = []
normalize = False

# Open the text file for reading
with open("results/results_cbt.exp1.txt", "r") as file:
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
    if entry[0] not in sudoku_stats:
        sudoku_stats[entry[0]] = {}

    if entry[1] not in sudoku_stats[entry[0]]:
        sudoku_stats[entry[0]][entry[1]] = {}

    sudoku_stats[entry[0]][entry[1]][entry[2]] = entry[3]

average_ct = {}
for solver, results in sudoku_stats.items():
    # normalized_stats = {}
    # stats = {}
    # for try_n, stat in tries.items():
    #     all_values = [values for stat in tries.values() for values in stat.values()]
    #     #/(sum(all_values)/len(all_values))
    #     values = zip(stat.keys(), [switches for oc, switches in stat.items()])
    #     for oc, n_switches in values:
    #         if oc not in stats:
    #             stats[oc] = []
    #
    #         stats[oc].append(float(n_switches))

    #all_values = [values for variants in results.values() for values in variants.values()]

    for n_fixed_values, variants in results.items():
        if solver not in average_ct:
            average_ct[solver] = {}

        average_ct[solver][n_fixed_values] = sum(variants.values()) / len(variants)

    if normalize:
        for solver, results in average_ct.items():
            for n_fixed_values, average in results.items():
                average_ct[solver][n_fixed_values] = average / max(average_ct[solver].values())

# Calculating the average for each (optimization credit, sudoku) pair
# for key in average_switches_per_sudoku:
#     average_switches_per_sudoku[key] = sum(average_switches_per_sudoku[key]) / len(average_switches_per_sudoku[key])

# Preparing data for plotting
# x_values = [key[0] for key in average_switches_per_sudoku.keys()]  # Optimization credits
# y_values = list(average_switches_per_sudoku.values())             # Averaged number of switches

# Creating the scatter plot
plt.figure(figsize=(12, 8))

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

# x_values = [key[0] for key in average_switches_per_sudoku.keys()]
# y_values = [average_switches_per_sudoku[key] for key in average_switches_per_sudoku.keys()]

# x_values = [key for key in average_ct.keys()]
# y_values = [average_ct[key] for key in average_ct.keys()]

#plt.scatter(x_values, y_values, color='blue')

# Adding a legend
plt.legend(plots, ['CBT', 'FWC', 'MCV'])
plt.gca().invert_xaxis()

# Fit a line (polynomial fit)
# Perform linear regression
slope, intercept, _, _, _ = linregress(x_values, y_values)

# Calculate the best-fit line
best_fit = slope * np.array(x_values) + intercept

# Plot the best-fit line
# plt.plot(x_values, best_fit, color='red', label='Best Fit Line (Linear Regression)')

plt.xticks(np.arange(min(x_values), max(x_values)+1, step=1))

plt.annotate(y_values[0], (10, y_values[0]), xytext=(0, 15), textcoords='offset points', ha='center', va='bottom', fontsize=8,
                 bbox=dict(boxstyle='round,pad=1', fc='white', alpha=0.8))

plt.title('CBT vs FWC vs MCV: Computing Time vs. #Fixed Values')
plt.ylabel('Computing Time (normalized)')
plt.xlabel('#Fixed Values')
plt.grid(True)
plt.show()
