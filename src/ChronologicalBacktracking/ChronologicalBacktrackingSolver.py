import math
import sys
import numpy as np

from src.Solver import Solver
from src.Sudoku.Sudoku import Sudoku
from src.Sudoku.Sudoku import SudokuHelper
import array as arr
from itertools import chain


#The class of the CBT algorithm
class ChronologicalBacktrackingSolver(Solver):
    steps_forward = 0
    steps_backward = 0

    #The algorithm method which takes in a start situation
    def solve(self, initial_values):
        # reset statistics
        self.steps_forward = 0
        self.steps_backward = 0

        # 1. create mask for uneditable numbers
        self.mask = SudokuHelper.create_mask(initial_values)

        initial_values = np.array(initial_values)

        # 2. Define our start situation to be a sudoku
        self.sudoku = Sudoku(initial_values)

        # 3. Start recursive solve
        if self.solve_element():
            self.finished = True

        # if verbose, then print stuff
        if self.verbose:
            print()
            print('Finished.')

        # return solved sudoku.
        return self.sudoku.values

    def is_valid(self, row, col, value):
        # horizontally correct
        if arr.array('i', self.sudoku.values[row, :]).count(value) > 1:
            return False

        # vertically correct
        if arr.array('i', self.sudoku.values[:, col]).count(value) > 1:
            return False

        # locally correct (cube 3x3)
        cube = SudokuHelper.get_cube(row, col)
        cube_values = list(chain.from_iterable(SudokuHelper.get_cube_values(self.sudoku.values, cube)))
        if arr.array('i', cube_values).count(value) > 1:
            return False

        return True

    def solve_element(self, element_n = 0):
        # Update stats
        self.steps_forward = self.steps_forward + 1

        # When element to handle is bigger than 81 (9*9), we are done. Success!
        if element_n > ((9*9) -1):
            return True

        # Get row and column of element to handle.
        row = SudokuHelper.get_row_by_element_number(element_n)
        col = SudokuHelper.get_col_by_element_number(element_n)

        # If element is uneditable, then directly go forward to next element in line.
        if self.mask[row, col] != 0:
            if not self.solve_element(element_n + 1):
                self.steps_backward = self.steps_backward + 1
                return False

            return True

        # Loop over the domain (all possible values).
        domain = self.get_domain(row, col)
        for value in domain:
            # Fill value in sudoku.
            self.sudoku.values[row][col] = value

            # Check if the sudoku is valid after filling value. If not, go to next one in loop (domain).
            if not self.is_valid(row, col, value):
                continue

            # Show a live log when solving a sudoku if on verbose
            if self.verbose:
                if self.steps_forward % 500 == 0:
                    sys.stdout.write(
                        f"\rSteps forward: {self.steps_forward}, "
                        f"Steps backward: {self.steps_backward}"
                    )
                    sys.stdout.flush()

            # Sudoku is still valid, go forward to next element. If next element returns
            # True, sudoku is solved, else path is not a partial solution: go on in loop.
            if self.solve_element(element_n + 1):
                return True

        # All tried values were invalid, reset value in sudoku, update stats
        # and return False so that above statement can go on in it's loop.
        self.sudoku.values[row][col] = 0
        self.steps_backward = self.steps_backward + 1

        return False

    def get_domain(self, row, col):
        # CBT domains are always 1-9.
        return range(1, 10)
