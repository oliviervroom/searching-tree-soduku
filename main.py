from renderer import Renderer
from solver import Solver
import time
import json

puzzle1 = [
    [0, 0, 3, 0, 2, 0, 6, 0, 0],
    [9, 0, 0, 3, 0, 5, 0, 0, 1],
    [0, 0, 1, 8, 0, 6, 4, 0, 0],
    [0, 0, 8, 1, 0, 2, 9, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 6, 7, 0, 8, 2, 0, 0],
    [0, 0, 2, 6, 0, 9, 5, 0, 0],
    [8, 0, 0, 2, 0, 3, 0, 0, 9],
    [0, 0, 5, 0, 1, 0, 3, 0, 0]
]

puzzle2 = [
    [2, 0, 0, 0, 8, 0, 3, 0, 0],
    [0, 6, 0, 0, 7, 0, 0, 8, 4],
    [0, 3, 0, 5, 0, 0, 2, 0, 9],
    [0, 0, 0, 1, 0, 5, 4, 0, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 0, 2, 7, 0, 6, 0, 0, 0],
    [3, 0, 1, 0, 0, 7, 0, 4, 0],
    [7, 2, 0, 0, 4, 0, 0, 6, 0],
    [0, 0, 4, 0, 1, 0, 0, 0, 3]
]

puzzle2_solved = [
    [2, 4, 5, 9, 8, 1, 3, 7, 6],
    [1, 6, 9, 2, 7, 3, 5, 8, 4],
    [8, 3, 7, 5, 6, 4, 2, 1, 9],
    [9, 7, 6, 1, 2, 5, 4, 3, 8],
    [5, 1, 3, 4, 9, 8, 6, 2, 7],
    [4, 8, 2, 7, 3, 6, 9, 5, 1],
    [3, 9, 1, 6, 5, 7, 8, 4, 2],
    [7, 2, 8, 3, 4, 9, 1, 6, 5],
    [6, 5, 4, 8, 1, 2, 7, 9, 3]
]

puzzle3 = [
    [0, 0, 0, 0, 0, 0, 9, 0, 7],
    [0, 0, 0, 4, 2, 0, 1, 8, 0],
    [0, 0, 0, 7, 0, 5, 0, 2, 6],
    [1, 0, 0, 9, 0, 4, 0, 0, 0],
    [0, 5, 0, 0, 0, 0, 0, 4, 0],
    [0, 0, 0, 5, 0, 7, 0, 0, 9],
    [9, 2, 0, 1, 0, 8, 0, 0, 0],
    [0, 0, 3, 4, 0, 5, 9, 0, 0],
    [0, 5, 0, 7, 0, 0, 0, 0, 0]
]

puzzle4 = [
    [0, 3, 0, 0, 5, 0, 0, 4, 0],
    [0, 0, 8, 0, 1, 0, 5, 0, 0],
    [4, 6, 0, 0, 0, 0, 1, 2, 0],
    [0, 7, 0, 5, 0, 2, 0, 8, 0],
    [0, 0, 0, 6, 0, 3, 0, 0, 0],
    [0, 4, 0, 1, 0, 9, 0, 3, 0],
    [0, 2, 5, 0, 0, 0, 0, 9, 8],
    [0, 0, 1, 0, 2, 0, 6, 0, 0],
    [0, 8, 0, 0, 6, 0, 0, 2, 0]
]

puzzle5 = [
    [0, 2, 0, 8, 1, 0, 7, 4, 0],
    [7, 0, 0, 0, 0, 3, 1, 0, 0],
    [0, 9, 0, 0, 0, 2, 8, 0, 5],
    [0, 0, 9, 0, 4, 0, 0, 8, 7],
    [4, 0, 0, 2, 0, 8, 0, 0, 3],
    [1, 6, 0, 0, 3, 0, 2, 0, 0],
    [3, 0, 2, 7, 0, 0, 0, 6, 0],
    [0, 0, 5, 6, 0, 0, 0, 0, 8],
    [0, 7, 6, 0, 5, 1, 0, 9, 0]
]

# initiate algorithm
solver = Solver(puzzle2, puzzle2_solved)

puzzle = solver.solve(2, 10, 20, 100000)

if not solver.finished:
    print('Oops not found...')


print('\n')
renderer = Renderer(puzzle)
renderer.print()
exit()

results = {}
for random_credits in range(1, 20):
    for pattern_credits in range(0, 20):
        for plateau_credits in range(0, 50):
            for try_n in range(1,5):
                start_time = time.time()

                solver.init()
                solver.solve(random_credits, pattern_credits, plateau_credits)

                end_time = time.time()
                elapsed_time = end_time - start_time

                if solver.finished:
                    print((random_credits, pattern_credits, plateau_credits, try_n), elapsed_time)
                    results[(random_credits, pattern_credits, plateau_credits, try_n)] = elapsed_time


# File path where you want to save the JSON
file_path = 'results.json'

# Writing JSON data
with open(file_path, 'w') as json_file:
    json.dump(results, json_file, indent=4)
