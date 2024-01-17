import math

import numpy as np

from src.Sudoku.Sudoku import Sudoku


#The class of the algorithm
class Solver:
    finished = False
    verbose = False

    sudoku = None
    mask = None

    n_of_switches = 0

    #Constructor method which takes parameters arguments (standard configuration is optimal)
    def __init__(self, verbose=True):
        self.verbose = verbose

    #The algorithm method which takes in a start situation
    def solve(self, initial_values):
        initial_values = np.array(initial_values)

        #Define our start situation to be a sudoku
        self.sudoku = Sudoku(initial_values)

        tries = 0


        if self.verbose:
            if tries > 1000:
                print('')

            print('Finished.')

        return self.sudoku.values