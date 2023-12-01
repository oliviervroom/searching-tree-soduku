import numpy as np
import math
import random

class Solver:

    def solve(self, puzzle):
        puzzle = np.array(puzzle)

        #... do solve

        # 1. create mask for uneditable numbers
        mask = self.create_mask(puzzle)

        # 2. for every cube fill numbers so that we have numbers 1-9
        puzzle = self.fill_zero_values(puzzle)

        # 3.

        row_evaluations = [self.evaluate_list(puzzle[row]) for row in range(0,9)]
        col_evaluations = [self.evaluate_list(self.flatten_list(puzzle[0:9, col:col+1])) for col in range(0,9)]

        s = 5
        finished = False

        while not finished:

            highest_row_eval = max(row_evaluations)
            highest_col_eval = max(col_evaluations)

            row_i = row_evaluations.index(highest_row_eval) + 1
            col_i = col_evaluations.index(highest_col_eval) + 1

            cube_n = (((row_i/3) - 1) * 3) + math.ceil(col_i / 3)

            # @todo test other implementation of s
            for switch_n in range(1, s+1):
                highest_local_row_eval = max(row_evaluations[self.get_row_start(cube_n):self.get_row_end(cube_n)])
                highest_local_col_eval = max(col_evaluations[self.get_col_start(cube_n):self.get_col_end(cube_n)])

                row_i = row_evaluations.index(highest_local_row_eval) + 1
                col_i = col_evaluations.index(highest_local_col_eval) + 1

                scope_values = []
                scope_mask = []
                if highest_local_row_eval > highest_local_col_eval:
                    # lock row
                    for row in range(self.get_row_start(cube_n)+1, self.get_row_end(cube_n)+1):
                        if row == row_i:
                            continue

                        scope_values.append(puzzle[row-1][self.get_col_start(cube_n):self.get_col_end(cube_n)])
                        scope_mask.append(mask[row-1][self.get_col_start(cube_n):self.get_col_end(cube_n)])

                print(scope_values)
                print(scope_mask)

                scope_values = self.flatten_list(scope_values)
                scope_mask = self.flatten_list(scope_mask)

                while True:
                    i = random.randint(1, 9) - 1

                    locked = False # @todo check wheter should be locked
                    if scope_mask[i] == 0 and not locked:
                        print(i)
                        exit()

                        puzzle[row_i][col_i] = scope_values[i]


                        break

                exit()

                row_i = row_evaluations.index(highest_row_eval) + 1
                col_i = col_evaluations.index(highest_col_eval) + 1

                cube_n = (((row_i / 3) - 1) * 3) + math.ceil(col_i / 3)

                row_range = range(self.get_row_start(cube_n), self.get_col_end(cube_n))
                col_range = range(self.get_col_start(cube_n), self.get_col_end(cube_n))

                heuristic_values = [self.evaluate_list(puzzle[row]) for row in row_range]



        return puzzle

    def create_mask(self, puzzle):
        mask = puzzle.copy()
        mask[mask > 0] = 1

        return mask

    def fill_zero_values(self, puzzle):

        for cube_n in range(1,10):
            cube_values = self.get_cube_values(puzzle, cube_n)

            flatList = self.flatten_list(cube_values)

            for number in range(1,10):
                if number not in flatList:
                    for i, value in enumerate(flatList):
                        if value == 0:
                            flatList[i] = number
                            break

            puzzle[self.get_row_start(cube_n):self.get_row_end(cube_n), self.get_col_start(cube_n):self.get_col_end(cube_n)] = [flatList[i:i + 3] for i in range(0, len(flatList), 3)]

        return puzzle

    def evaluate_list(self, list):
        return int(9 - len(set(list)))

    def get_col_start(self, cube):
        return int(((cube - 1) % 3) * 3)

    def get_col_end(self, cube):
        return int(((cube - 1) % 3) * 3 + 3)

    def get_row_start(self, cube):
        return int((math.ceil(cube / 3) - 1) * 3)

    def get_row_end(self, cube):
        return int((math.ceil(cube / 3) - 1) * 3 + 3)

    def get_cube_values(self, puzzle, cube_n):
        return puzzle[
           self.get_row_start(cube_n):self.get_row_end(cube_n),
           self.get_col_start(cube_n):self.get_col_end(cube_n)
       ]

    def flatten_list(self, list):
        return [item for sublist in list for item in sublist]
