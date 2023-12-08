from renderer import Renderer
from solver import Solver
import time
import uuid
import math
import numpy

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

puzzle = [
    [
        [0, 0, 3, 0, 2, 0, 6, 0, 0],
        [9, 0, 0, 3, 0, 5, 0, 0, 1],
        [0, 0, 1, 8, 0, 6, 4, 0, 0],
        [0, 0, 8, 1, 0, 2, 9, 0, 0],
        [7, 0, 0, 0, 0, 0, 0, 0, 8],
        [0, 0, 6, 7, 0, 8, 2, 0, 0],
        [0, 0, 2, 6, 0, 9, 5, 0, 0],
        [8, 0, 0, 2, 0, 3, 0, 0, 9],
        [0, 0, 5, 0, 1, 0, 3, 0, 0]
    ],
    [
        [2, 0, 0, 0, 8, 0, 3, 0, 0],
        [0, 6, 0, 0, 7, 0, 0, 8, 4],
        [0, 3, 0, 5, 0, 0, 2, 0, 9],
        [0, 0, 0, 1, 0, 5, 4, 0, 8],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 0, 2, 7, 0, 6, 0, 0, 0],
        [3, 0, 1, 0, 0, 7, 0, 4, 0],
        [7, 2, 0, 0, 4, 0, 0, 6, 0],
        [0, 0, 4, 0, 1, 0, 0, 0, 3]
    ],
    [
        [0, 0, 0, 0, 0, 0, 9, 0, 7],
        [0, 0, 0, 4, 2, 0, 1, 8, 0],
        [0, 0, 0, 7, 0, 5, 0, 2, 6],
        [1, 0, 0, 9, 0, 4, 0, 0, 0],
        [0, 5, 0, 0, 0, 0, 0, 4, 0],
        [0, 0, 0, 5, 0, 7, 0, 0, 9],
        [9, 2, 0, 1, 0, 8, 0, 0, 0],
        [0, 3, 4, 0, 5, 9, 0, 0, 0],
        [5, 0, 7, 0, 0, 0, 0, 0, 0]
    ],
    [
        [0, 3, 0, 0, 5, 0, 0, 4, 0],
        [0, 0, 8, 0, 1, 0, 5, 0, 0],
        [4, 6, 0, 0, 0, 0, 0, 1, 2],
        [0, 7, 0, 5, 0, 2, 0, 8, 0],
        [0, 0, 0, 6, 0, 3, 0, 0, 0],
        [0, 4, 0, 1, 0, 9, 0, 3, 0],
        [2, 5, 0, 0, 0, 0, 0, 9, 8],
        [0, 0, 1, 0, 2, 0, 6, 0, 0],
        [0, 8, 0, 0, 6, 0, 0, 2, 0]
    ],
    [
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
]

execution_key = uuid.uuid4()

# File path where you want to save the JSON
file_path = f'results/results_{execution_key}.txt'

for optimization_credits in range(5, 20):
    for random_credits in [5]:
        for pattern_credits in [0]:
            for plateau_credits in [0]:
                for sudoku in range(0,5):
                    for try_n in range(1,4):
                        # initiate algorithm
                        solver = Solver(optimization_credits, random_credits, pattern_credits, plateau_credits)

                        start_time = time.time()

                        solver.solve(puzzle[sudoku])

                        end_time = time.time()
                        elapsed_time = end_time - start_time

                        if solver.finished:
                            if sudoku == 1:
                                if not numpy.array_equal(numpy.array(solver.sudoku.values), numpy.array(puzzle2_solved)):
                                    print('not correct!')

                            print((optimization_credits, random_credits, pattern_credits, plateau_credits, sudoku, try_n), elapsed_time, 'Switches:', solver.switches, 'NO:', solver.n_new_optimums, 'SO:', solver.n_same_optimums, 'PLT', solver.n_plateaus, 'PTRN', solver.n_patterns, 'RW', solver.n_random_walks)

                            # Writing JSON data
                            with open(file_path, 'a') as file:
                                file.write([(optimization_credits, random_credits, pattern_credits, plateau_credits, sudoku, try_n), elapsed_time, 'Switches:', solver.switches, 'NO:', solver.n_new_optimums, 'SO:', solver.n_same_optimums, 'PLT', solver.n_plateaus, 'PTRN', solver.n_patterns, 'RW', solver.n_random_walks].__str__() + '\n')
                        else:
                            print('Failed')
                            print((optimization_credits, random_credits, pattern_credits, plateau_credits, sudoku, try_n), elapsed_time, 'Switches:', solver.switches, 'NO:', solver.n_new_optimums, 'SO:', solver.n_same_optimums, 'PLT', solver.n_plateaus, 'PTRN', solver.n_patterns, 'RW', solver.n_random_walks)
