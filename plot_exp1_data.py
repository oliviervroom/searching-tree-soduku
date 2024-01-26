import matplotlib.pyplot as plt
from matplotlib.table import Table
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
    if entry[1] not in sudoku_stats:
        sudoku_stats[entry[1]] = {}

    if entry[0] not in sudoku_stats[entry[1]]:
        sudoku_stats[entry[1]][entry[0]] = {}

    sudoku_stats[entry[1]][entry[0]] = entry[6]

print(sudoku_stats)
exit()

average_ct = {}
for solver, results in sudoku_stats.items():
    average_ct[solver] = sum(results.values()) / len(results)

average_ct = {k: average_ct[k] for k in sorted(average_ct)}

# Create a figure and a subplot (which we won't use, but it's necessary to create the table)
fig, ax = plt.subplots()

# Hide axes
ax.axis('tight')
ax.axis('off')

# Sample data for the table
data = [['Apple', 10], ['Banana', 20], ['Orange', 30], ['Pear', 40]]
columns = ['Fruit', 'Quantity']

# Create a table and add it to the axes
table = Table(ax, bbox=[0, 0, 1, 1])

# Adding cells
for i in range(len(data)+1):
    for j in range(len(columns)):
        if i == 0:
            # Header row
            cell_text = columns[j]
            table.add_cell(i, j, 0.2, 0.1, text=cell_text, loc='center', facecolor='lightblue')
        else:
            # Data rows
            cell_text = data[i-1][j]
            table.add_cell(i, j, 0.2, 0.1, text=cell_text, loc='center')

# Add the table to the axes
ax.add_table(table)

plt.show()
