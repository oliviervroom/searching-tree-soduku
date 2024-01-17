import math

import numpy as np

from src.Solver import Solver
from src.Sudoku.Sudoku import Sudoku
from src.Sudoku.Sudoku import SudokuHelper
import array as arr
from itertools import chain


#The class of the algorithm
class ChronologicalBacktrackingSolver(Solver):

    #The algorithm method which takes in a start situation
    def solve(self, initial_values):
        # 1. create mask for uneditable numbers
        self.mask = SudokuHelper.create_mask(initial_values)

        initial_values = np.array(initial_values)

        #Define our start situation to be a sudoku
        self.sudoku = Sudoku(initial_values)

        if self.solve_element():
            self.finished = True

        if self.verbose:
            print('Finished.')

        return self.sudoku.values

    def is_valid(self, row, col, value):
        # horizontally correct
        if arr.array('i', self.sudoku.values[row, :]).count(value) > 1:
            return False

        # vertically correct
        if arr.array('i', self.sudoku.values[:, col]).count(value) > 1:
            return False

        # locally correct
        cube = SudokuHelper.get_cube(row, col)
        cube_values = list(chain.from_iterable(SudokuHelper.get_cube_values(self.sudoku.values, cube)))
        if arr.array('i', cube_values).count(value) > 1:
            return False

        return True

    def solve_element(self, element_n = 0):
        if element_n > ((9*9) -1):
            return True

        row = SudokuHelper.get_row_by_element_number(element_n)
        col = SudokuHelper.get_col_by_element_number(element_n)

        if self.mask[row, col] != 0:
            return self.solve_element(element_n + 1)

        for value in self.get_domain(row, col):
            self.sudoku.values[row][col] = value

            if not self.is_valid(row, col, value):
                continue

            if self.solve_element(element_n + 1):
                return True

        self.sudoku.values[row][col] = 0

        return False

    def get_domain(self, row, col):
        return range(1, 10)