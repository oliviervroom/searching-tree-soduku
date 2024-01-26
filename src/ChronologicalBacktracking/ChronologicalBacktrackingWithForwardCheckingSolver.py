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
        # reset statistics
        self.steps_forward = 0
        self.steps_backward = 0

        # 1. create mask for uneditable numbers
        self.mask = SudokuHelper.create_mask(initial_values)

        initial_values = np.array(initial_values)

        # 2. Define our start situation to be a sudoku
        self.sudoku = Sudoku(initial_values)

        # 3. Make all domains up-to-date.
        self.domains = {}
        for row in range(0, 9):
            for column in range(0, 9):
                self.update_domain(row, column)

        # 3. Start recursive solve
        if self.solve_element():
            self.finished = True

        # if verbose, then print stuff
        if self.verbose:
            print()
            print('Finished.')

        # return solved sudoku.
        return self.sudoku.values

    def solve_element(self, element_n = 0):
        # Update stats
        self.steps_forward = self.steps_forward + 1

        # When element to handle is bigger than 81 (9*9), we are done. Success!
        if element_n > ((9 * 9) - 1):
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

            # Update domains of related fields of current coord. If update
            # was aborted, then there was a empty domain, meaning invalid
            # sudoku: go on to next in loop/domain.
            if not self.update_domains(row, col):
                continue

            # Show a live log when solving a sudoku
            if self.verbose:
                if self.steps_forward % 500 == 0:
                    sys.stdout.write(
                        f"\rSteps forward: {self.steps_forward}, "
                        f"Steps backward: {self.steps_backward}, "
                    )
                    sys.stdout.flush()

            # Go forward to next element. If next element returns True, sudoku
            # is solved, else path is not a partial solution: go on in loop
            if self.solve_element(element_n + 1):
                return True

        # All tried values were not a partial solution. Reset value in sudoku,
        # update related domains, update stats and return False so that above
        # statement can go on in it's loop.
        self.sudoku.values[row][col] = 0
        self.update_domains(row, col)
        self.steps_backward = self.steps_backward + 1

        return False

    def update_domains(self, row, column):
        # Update it's own domain
        self.update_domain(row, column)

        # Loop over all vertical columns
        for r in range(0,9):
            # Skip it's own coord
            if r == row:
                continue

            # Skip if coord is uneditable
            if self.mask[r][column] != 0:
                continue

            # Update domain of coord. If updated domain is empty and field is
            # unvisited, meaning not filled, abort whole update action: invalid.
            if len(self.update_domain(r, column)) == 0 and self.sudoku.values[r][column] == 0:
                return False

        for c in range(0,9):
            # Skip it's own coord
            if c == column:
                continue

            # Skip if coord is uneditable
            if self.mask[row][c] != 0:
                continue

            # Update domain of coord. If updated domain is empty and field is
            # unvisited, meaning not filled, abort whole update action: invalid.
            if len(self.update_domain(row, c)) == 0 and self.sudoku.values[row][c] == 0:
                return False

        # Determine cube number and its coord range.
        cube = SudokuHelper.get_cube(row, column)
        base_row = SudokuHelper.get_row_start(cube)
        base_col = SudokuHelper.get_col_start(cube)

        for r in range(0, 3):
            # Skip it's own coord
            if r == row:
                continue

            for c in range(0, 3):
                # Skip it's own coord
                if c == column:
                    continue

                # Skip if coord is uneditable
                if self.mask[base_row+r][base_col+c] != 0:
                    continue

                # Update domain of coord. If updated domain is empty and field is
                # unvisited, meaning not filled, abort whole update action: invalid.
                if len(self.update_domain(base_row + r, base_col + c)) == 0 and self.sudoku.values[base_row + r][base_col + c] == 0:
                    return False

        # successful
        return True

    def update_domain(self, row, column):
        # Skip if coord is uneditable
        if self.mask[row][column] != 0:
            return

        # Determine cube number and all its values.
        cube = SudokuHelper.get_cube(row, column)
        cube_values = list(chain.from_iterable(SudokuHelper.get_cube_values(self.sudoku.values, cube)))

        # Combine all cube values, row values and column values, put it in a list to
        # make it unique and use it as values to exclude from a fresh domain.
        values_to_exclude = list(set(list(chain(self.sudoku.values[row, :], self.sudoku.values[:, column], cube_values))))
        self.domains[(row, column)] = list(filter(lambda x: x not in values_to_exclude, list(range(1,10))))

        # Return domain so that empty domains can be noticed.
        return self.domains[(row, column)]

    def get_domain(self, row, column):
        # Return domain from domain list.
        return self.domains[(row, column)]
