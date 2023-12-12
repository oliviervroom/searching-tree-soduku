import matplotlib.pyplot as plt
from collections import defaultdict

#to-do: normalize the value by dividing value by max value of its own sudoku, for instance sudoku 5 had a highest value at credits


# Complete dataset with three tries per sudoku for each set of parameters
# data = [
# [(5, 5, 0, 0, 0, 1), 2.1815807819366455, 'Switches:', 5078, 'NO:', 604, 'SO:', 8416, 'PLT', 0, 'PTRN', 0, 'RW', 291]
# [(5, 5, 0, 0, 0, 2), 0.1922166347503662, 'Switches:', 557, 'NO:', 77, 'SO:', 776, 'PLT', 0, 'PTRN', 0, 'RW', 24]
# ]
# In order from left to right, with examples from the first one to clarify:
# 1st: optimization credits (e.g. 5)
# 2nd: random credits (5)
# 3rd: pattern credits (0)
# 4th: plateau credits (0)
# 5th: sudoku (0)
# 6th: Try (1)
# 7: time (2.18...)

# Initialize an empty list to store the extracted data
data = []

# Open the text file for reading
with open("results_best-imp.exp1.txt", "r") as file:
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

# Print the resulting list
#for entry in data:
 #   print(entry)
print(data)



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
        all_values = [switches for switches in stat.items() for stat in tries.items()]
        values = zip(stat.keys(), [switches/max(all_values) for oc, switches in stat.items()])
        for oc, n_switches in values:
            if oc not in stats:
                stats[oc] = []

            stats[oc].append(n_switches)
    print(stats)
    exit()
    average_stats = {}
    for oc, values in stats.items():
        key = (oc, sudoku)
        average_switches_per_sudoku[key].append(sum(values) / len(values))

# Calculating the average for each (optimization credit, sudoku) pair
for key in average_switches_per_sudoku:
    average_switches_per_sudoku[key] = sum(average_switches_per_sudoku[key]) / len(average_switches_per_sudoku[key])

# Preparing data for plotting
# x_values = [key[0] for key in average_switches_per_sudoku.keys()]  # Optimization credits
# y_values = list(average_switches_per_sudoku.values())             # Averaged number of switches

# Creating the scatter plot
plt.figure(figsize=(12, 8))

# Assign a unique color to each Sudoku
colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'orange', 'purple', 'brown']
color_index = 0

for sudoku in set(key[1] for key in average_switches_per_sudoku.keys()):
    # Filter the data for the current Sudoku
    x_values = [key[0] for key in average_switches_per_sudoku.keys() if key[1] == sudoku]
    y_values = [average_switches_per_sudoku[key] for key in average_switches_per_sudoku.keys() if key[1] == sudoku]

    # Plot the data for the current Sudoku
    plt.scatter(x_values, y_values, color=colors[color_index], label=f'Sudoku {sudoku}')
    color_index = (color_index + 1) % len(colors)

plt.title('Average #switches vs. Optimization Credits for Each Sudoku')
plt.xlabel('Optimization Credits')
plt.ylabel('Average #switches')
plt.grid(True)
plt.show()
