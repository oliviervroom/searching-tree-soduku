import math
import array
from src.ChronologicalBacktracking.ChronologicalBacktrackingSolver import ChronologicalBacktrackingSolver
from src.Sudoku.SudokuHelper import SudokuHelper
from src.Sudoku.Sudoku import Sudoku
import numpy as np
from itertools import chain
import sys

#The class of the algorithm
class ChronologicalBacktrackingWithForwardCheckingSolver(ChronologicalBacktrackingSolver):
    domains = None

    # The algorithm method which takes in a start situation
    def solve(self, initial_values):
        self.steps_forward = 0
        self.steps_backward = 0

        # 1. create mask for uneditable numbers
        self.mask = SudokuHelper.create_mask(initial_values)

        initial_values = np.array(initial_values)

        # Define our start situation to be a sudoku
        self.sudoku = Sudoku(initial_values)

        self.domains = {}
        for row in range(0, 9):
            for column in range(0, 9):
                self.update_domain(row, column)

        if self.solve_element():
            self.finished = True

        if self.verbose:
            print()
            print('Finished.')

        return self.sudoku.values

    def solve_element(self, element_n = 0):
        self.steps_forward = self.steps_forward + 1

        if element_n > ((9 * 9) - 1):
            return True

        row = SudokuHelper.get_row_by_element_number(element_n)
        col = SudokuHelper.get_col_by_element_number(element_n)

        if self.mask[row, col] != 0:
            if not self.solve_element(element_n + 1):
                self.steps_backward = self.steps_backward + 1
                return False

            return True

        domain = self.get_domain(row, col)
        for value in domain:
            self.sudoku.values[row][col] = value

            if not self.update_domains(row, col):
                continue

            # show a live log when solving a sudoku
            if self.verbose:
                if self.steps_forward % 500 == 0:
                    sys.stdout.write(
                        f"\rSteps forward: {self.steps_forward}, "
                        f"Steps backward: {self.steps_backward}, "
                    )
                    sys.stdout.flush()

            if self.solve_element(element_n + 1):
                return True

        self.sudoku.values[row][col] = 0
        self.update_domains(row, col)
        self.steps_backward = self.steps_backward + 1

        return False

    def update_domains(self, row, column):
        self.update_domain(row, column)

        for r in range(0,9):
            if r == row:
                continue

            if self.mask[r][column] != 0:
                continue

            if len(self.update_domain(r, column)) == 0 and self.sudoku.values[r][column] == 0:
                return False

        for c in range(0,9):
            if c == column:
                continue

            if self.mask[row][c] != 0:
                continue

            if len(self.update_domain(row, c)) == 0 and self.sudoku.values[row][c] == 0:
                return False

        cube = SudokuHelper.get_cube(row, column)
        base_row = SudokuHelper.get_row_start(cube)
        base_col = SudokuHelper.get_col_start(cube)

        for r in range(0, 3):
            if r == row:
                continue

            for c in range(0, 3):
                if c == column:
                    continue

                if self.mask[base_row+r][base_col+c] != 0:
                    continue

                if len(self.update_domain(base_row + r, base_col + c)) == 0 and self.sudoku.values[base_row + r][base_col + c] == 0:
                    return False

        return True

    def update_domain(self, row, column):
        if self.mask[row][column] != 0:
            return

        cube = SudokuHelper.get_cube(row, column)
        cube_values = list(chain.from_iterable(SudokuHelper.get_cube_values(self.sudoku.values, cube)))

        values_to_exclude = list(set(list(chain(self.sudoku.values[row, :], self.sudoku.values[:, column], cube_values))))
        self.domains[(row, column)] = list(filter(lambda x: x not in values_to_exclude, list(range(1,10))))

        return self.domains[(row, column)]

    def get_domain(self, row, column):
        return self.domains[(row, column)]
