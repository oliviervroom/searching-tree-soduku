from src.Renderer import Renderer
from src.SudokuGenerator import SudokuGenerator
from src.LocalSearch.LocalSearchSolver import LocalSearchSolver
from src.LocalSearch.LocalSearchApproach import LocalSearchApproach
from src.ChronologicalBacktracking.ChronologicalBacktrackingSolver import ChronologicalBacktrackingSolver
from src.ChronologicalBacktracking.ChronologicalBacktrackingWithForwardCheckingSolver import ChronologicalBacktrackingWithForwardCheckingSolver
from src.ChronologicalBacktracking.ChronologicalBacktrackingWithForwardCheckingAndMostConstrainedVariable import ChronologicalBacktrackingWithForwardCheckingAndMostConstrainedVariable
import time
from data.assignment_puzzles import assignment_puzzles
from enum import Enum


class PrintStyle(Enum):
    CONSOLE = 0
    WINDOW = 1

# For TA:
# - Paste a puzzle below (string or list style)
sudoku_puzzle = '0 2 0 8 1 0 7 4 0 7 0 0 0 0 3 1 0 0 0 9 0 0 0 2 8 0 5 0 0 9 0 4 0 0 8 7 4 0 0 2 0 8 0 0 3 1 6 0 0 3 0 2 0 0 3 0 2 7 0 0 0 6 0 0 0 5 6 0 0 0 0 8 0 7 6 0 5 1 0 9 0'
sudoku_puzzle = [[0, 0, 3, 0, 2, 0, 6, 0, 0], [9, 0, 0, 3, 0, 5, 0, 0, 1], [0, 0, 1, 8, 0, 6, 4, 0, 0],
                 [0, 0, 8, 1, 0, 2, 9, 0, 0], [7, 0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 6, 7, 0, 8, 2, 0, 0],
                 [0, 0, 2, 6, 0, 9, 5, 0, 0], [8, 0, 0, 2, 0, 3, 0, 0, 9], [0, 0, 5, 0, 1, 0, 3, 0, 0]]

# - Or take one of the assignment puzzles (0-4)
sudoku_puzzle = assignment_puzzles[2]

# - How do you want to view the results?
print_style = PrintStyle.CONSOLE

# - Do you want to monitor the process?
verbose = True

if not isinstance(sudoku_puzzle, list):
    # Check that pasted_sudoku is 161 characters long (including spaces)
    if len(sudoku_puzzle) != 161:
        print('Pasted Sudoku is not 161 characters long (including spaces)! Instead, it is: ')
        print(len(sudoku_puzzle))
        exit()

    # Check that pasted_sudoku is only numbers and spaces
    if not sudoku_puzzle.replace(' ', '').isdigit():
        print('Sudoku contains non-numeric characters')
        exit()

    # Turn pasted_sudoku into a list of lists to make it easier to load into the solver
    sudoku_puzzle = [int(x) for x in sudoku_puzzle.split()]
    sudoku_puzzle = [sudoku_puzzle[i:i + 9] for i in range(0, len(sudoku_puzzle), 9)]

# Initiate solving algorithm
solver1 = ChronologicalBacktrackingSolver(verbose=verbose)
solver2 = ChronologicalBacktrackingWithForwardCheckingSolver(verbose=verbose)
solver3 = ChronologicalBacktrackingWithForwardCheckingAndMostConstrainedVariable(verbose=verbose)

solvers = [solver2]

# sudoku_puzzle = SudokuGenerator.get_sudoku(17)[2]
# start_time = time.time()
#
# solver3.solve(sudoku_puzzle)
#
# end_time = time.time()
# elapsed_time = end_time - start_time
#
# if solver3.finished:
#     print('Elapsed time in seconds:', elapsed_time)
#
# exit()

# File path where you want to save the JSON
file_path = f'results/results_cbt.exp1.txt'

fixed_values = list(range(0, 36))
fixed_values.reverse()

for solver in solvers:
    for n_fixed_values in fixed_values:
        print('Number of fixed values processing: ' + str(n_fixed_values))

        sudoku_puzzles = SudokuGenerator.get_sudoku(n_fixed_values)

        for sudoku_puzzle in sudoku_puzzles:
            variant_key = sudoku_puzzles.index(sudoku_puzzle)
            start_time = time.time()

            solver.solve(sudoku_puzzle)

            end_time = time.time()
            elapsed_time = end_time - start_time

            with open(file_path, 'a') as file:
                file.write([(solvers.index(solver), n_fixed_values, variant_key), elapsed_time, 'SF:', solver.steps_forward, 'SB:', solver.steps_backward].__str__() + '\n')

            # Print the solved puzzle and the results
            if solver.finished:
                print('Elapsed time in seconds:', elapsed_time, 'Total switches:', solver.n_of_switches)

                if print_style == PrintStyle.WINDOW:
                    Renderer(solver.sudoku.values).render()
                elif print_style == PrintStyle.CONSOLE:
                    Renderer(solver.sudoku.values).print()

            # Otherwise, print that the puzzle was not solved
            else:
                print('Failed')
