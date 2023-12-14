from renderer import Renderer
from solver import Solver, LocalSearchApproach
import time
import sys
import uuid
import math
import numpy


#For TA, paste sudoku below:
sudoku_puzzle = '0 2 0 8 1 0 7 4 0 7 0 0 0 0 3 1 0 0 0 9 0 0 0 2 8 0 5 0 0 9 0 4 0 0 8 7 4 0 0 2 0 8 0 0 3 1 6 0 0 3 0 2 0 0 3 0 2 7 0 0 0 6 0 0 0 5 6 0 0 0 0 8 0 7 6 0 5 1 0 9 0'


# #Check that pasted_sudoku is 161 characters long (including spaces)
if len(sudoku_puzzle) != 161:
    print('Pasted Sudoku is not 161 characters long (including spaces)! Instead, it is: ')
    print(len(sudoku_puzzle))
    exit()

#Check that pasted_sudoku is only numbers and spaces
if not sudoku_puzzle.replace(' ', '').isdigit():
    print('Sudoku contains non-numeric characters')
    exit()

#Turn pasted_sudoku into a list of lists to make it easier to load into the solver
sudoku_puzzle = [int(x) for x in sudoku_puzzle.split()]
sudoku_puzzle = [sudoku_puzzle[i:i+9] for i in range(0, len(sudoku_puzzle), 9)]




# initiate solving algorithm


solver = Solver(
optimization_credits=10,
random_credits=1,
pattern_credits=19,
plateau_credits=4,
local_search_approach=LocalSearchApproach.FIRST_IMPROVEMENT,
verbose=True)

start_time = time.time()

solver.solve(sudoku_puzzle)

end_time = time.time()
elapsed_time = end_time - start_time

#Print the solved puzzle and the results
if solver.finished:
    print('Elapsed time in seconds:', elapsed_time, 'Total switches:', solver.n_of_switches)
    Renderer(solver.sudoku.values).render()

#Otherwise, print that the puzzle was not solved
else:
    print('Failed')






