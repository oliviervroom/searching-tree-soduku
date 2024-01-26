from src.SudokuRepository import SudokuRepository
from src.LocalSearch.LocalSearchSolver import LocalSearchSolver
from src.LocalSearch.LocalSearchApproach import LocalSearchApproach
from src.ChronologicalBacktracking.ChronologicalBacktrackingSolver import ChronologicalBacktrackingSolver
from src.ChronologicalBacktracking.ChronologicalBacktrackingWithForwardCheckingSolver import ChronologicalBacktrackingWithForwardCheckingSolver
from src.ChronologicalBacktracking.ChronologicalBacktrackingWithForwardCheckingAndMostConstrainedVariable import ChronologicalBacktrackingWithForwardCheckingAndMostConstrainedVariable
from data.assignment_puzzles import assignment_puzzles
import time

# Initiate solving algorithm
solver1 = ChronologicalBacktrackingSolver(verbose=True)
solver2 = ChronologicalBacktrackingWithForwardCheckingSolver(verbose=True)
solver3 = ChronologicalBacktrackingWithForwardCheckingAndMostConstrainedVariable(verbose=True)

# Which solvers to generate test results from.
solvers = [solver1, solver2, solver3]

# File path where you want to save the data
file_path = f'results/results_cbt.exp2.txt'

fixed_values = list(range(0, 36))
fixed_values.reverse()

stop = False
for n_fixed_values in fixed_values:
    if stop:
        break

    print('Number of fixed values processing: ' + str(n_fixed_values))

    # Use SudokuRepository to get sudoku's by fixed values from our own samples collection.
    sudoku_puzzles = SudokuRepository.get_sudoku(n_fixed_values)

    # Loop over all sudoku's
    for sudoku_puzzle in sudoku_puzzles:
        for solver in solvers:
            variant_key = sudoku_puzzles.index(sudoku_puzzle)
            start_time = time.time()

            solver.solve(sudoku_puzzle)

            end_time = time.time()
            elapsed_time = end_time - start_time

            # Softly stop run if time of one sudoku solving goes over 5 minutes.
            if elapsed_time > 300:
                stop = True

            # Append results
            with open(file_path, 'a') as file:
                #(solvers.index(solver))
                file.write([n_fixed_values, variant_key, 2, elapsed_time, 'SF:', solver.steps_forward, 'SB:', solver.steps_backward].__str__() + '\n')

            # Print the solved puzzle and the results
            if solver.finished:
                print('Elapsed time in seconds:', elapsed_time, 'Total switches:', solver.n_of_switches)

            # Otherwise, print that the puzzle was not solved
            else:
                print('Failed')