import numpy as np
import math
import random

class Solver:
    alg_tries = 0

    def solve(self, initial_puzzle):
        puzzle = np.array(initial_puzzle)

        #... do solve

        # 1. create mask for uneditable numbers
        mask = self.create_mask(puzzle)

        # 2. for every cube fill numbers so that we have numbers 1-9
        #TODO verander de functie zodat de nummers eerst geshuffeld worden voordat ze iteratief de nullen vervangen.
        puzzle = self.fill_zero_values(puzzle)

        # 3. Calculate the evaluation of all rows and columns based on the randomly filled-in sudoku
        
        row_evaluations = [self.evaluate_list(puzzle[row]) for row in range(0,9)]
        col_evaluations = [self.evaluate_list(self.flatten_list(puzzle[0:9, col:col+1])) for col in range(0,9)]

        # 4. Locate the cube with the highest evaluated entry and switch within the cube to obtain 
        # a lower evaluation for the affected rows and columns
        #TODO Moet de switch binnen een lokaal de eerste verbetering doen of de beste verbetering opzoeken
        #TODO Zodra een switch is gedaan, moet er dan naar een andere waarde in het lokaal worden gekeken
        # of bekijken we dan de hoogste evaluatie van de hele sudoku
        s = 20
        finished = False
        # debug = True

        #print_on_debug = lambda *print : # print(*print) if debug else None

        # print(puzzle)

        #

        self.alg_tries += 1

        print('Tries:', self.alg_tries)

        tries = 0
        last_high = 99999
        while not finished:
            # print('')
            tries += 1

            highest_row_eval = max(row_evaluations)
            highest_col_eval = max(col_evaluations)

            # print(puzzle)
            # print(row_evaluations)
            # print(col_evaluations)
            current_high = sum(row_evaluations) + sum(col_evaluations)

            if current_high == last_high:
                tries += 1

            last_high = current_high

            if tries > 100:
                print('Eval:', current_high)
                break

            print('Total eval: ', last_high, tries)

            if (highest_row_eval + highest_col_eval) == 0:
                finished = True
                break

            # row_i = row_evaluations.index(highest_row_eval)
            # col_i = col_evaluations.index(highest_col_eval)

            #cube_n = 1 + (math.floor(row_i/3) * 3) + math.floor(col_i / 3)
            cube_n = random.randint(1,9)

            print('Cube:', cube_n)

            highest_local_row_eval = max(row_evaluations[self.get_row_start(cube_n):self.get_row_end(cube_n)])
            highest_local_col_eval = max(col_evaluations[self.get_col_start(cube_n):self.get_col_end(cube_n)])

            start_switch_row = ((math.ceil(cube_n / 3) - 1) * 3) + row_evaluations[self.get_row_start(cube_n):self.get_row_end(cube_n)].index(highest_local_row_eval)
            start_switch_col = (math.floor((cube_n - 1) % 3) + 1) + col_evaluations[self.get_col_start(cube_n):self.get_col_end(cube_n)].index(highest_local_col_eval)

            # print('Start switch:', start_switch_row, start_switch_col)

            # if highest_local_row_eval > highest_local_col_eval:
            #     is_locked = lambda row, col: row == start_switch_row
            # else:
            #     is_locked = lambda row, col: col == start_switch_col

            is_locked = lambda row, col : row == start_switch_row and col == start_switch_col

            s = 5

            last_eval_sum = sum(row_evaluations) + sum(col_evaluations)
            switch_tries = 0
            do_random = 0
            last_switch = None
            while True:
                random_switches = list(range(0, 8))
                random.shuffle(random_switches)

                switched = False

                for end_switch_i in random_switches:
                    cube_row_base = ((math.ceil((start_switch_row + 1) / 3) - 1) * 3)
                    cube_col_base = ((math.ceil((start_switch_col + 1) / 3) - 1) * 3)
                    end_switch_row = cube_row_base + math.ceil((end_switch_i+1) / 3) - 1
                    end_switch_col = cube_col_base + end_switch_i % 3

                    switch = (start_switch_row, start_switch_col), (end_switch_row, end_switch_col)

                    if mask[end_switch_row][end_switch_col] == 0 and not is_locked(end_switch_row, end_switch_col) and switch != last_switch:
                        virtual = puzzle.copy()

                        # get values
                        start_value = virtual[start_switch_row][start_switch_col]
                        end_value = virtual[end_switch_row][end_switch_col]

                        # switch values
                        virtual[start_switch_row][start_switch_col] = end_value
                        virtual[end_switch_row][end_switch_col] = start_value

                        rows = list({ start_switch_row, end_switch_row })
                        cols = list({ start_switch_col, end_switch_col })

                        old_rows_eval = sum([self.evaluate_list(row) for row in puzzle[rows]])
                        old_cols_eval = sum([self.evaluate_list([puzzle[row, col] for row in range(0, 9)]) for col in cols])

                        new_row_evals = [self.evaluate_list(row) for row in virtual[rows]]
                        new_rows_eval = sum(new_row_evals)
                        new_col_evals = [self.evaluate_list([virtual[row, col] for row in range(0, 9)]) for col in cols]
                        new_cols_eval = sum(new_col_evals)

                        if (new_rows_eval + new_cols_eval) <= (old_rows_eval + old_cols_eval):
                            puzzle = virtual

                            for row, eval in zip(rows, new_row_evals):
                                row_evaluations[row] = eval

                            for col, eval in zip(cols, new_col_evals):
                                col_evaluations[col] = eval

                            switched = True
                            last_switch = switch

                            break
                        elif do_random > 0:
                            do_random -= 1

                            puzzle = virtual

                            for row, eval in zip(rows, new_row_evals):
                                row_evaluations[row] = eval

                            for col, eval in zip(cols, new_col_evals):
                                col_evaluations[col] = eval

                            switched = True
                            last_switch = switch

                if not switched:
                    # optimum
                    print('optimum')

                    random = 3

                    break

                if last_eval_sum <= sum(row_evaluations) + sum(col_evaluations):
                    # plateau
                    switch_tries += 1

                    if switch_tries > s:
                        print('plateau')
                        break

                last_eval_sum = sum(row_evaluations) + sum(col_evaluations)

                # scope_values = self.flatten_list(scope_values)
                # scope_mask = self.flatten_list(scope_mask)
                #
                # while True:
                #     i = random.randint(1, 9) - 1
                #
                #     locked = False # @todo check wheter should be locked
                #     if scope_mask[i] == 0 and not locked:
                #         # print(i)
                #         exit()
                #
                #         puzzle[row_i][col_i] = scope_values[i]
                #
                #
                #         break
                #
                # exit()
                #
                # row_i = row_evaluations.index(highest_row_eval) + 1
                # col_i = col_evaluations.index(highest_col_eval) + 1
                #
                # cube_n = (((row_i / 3) - 1) * 3) + math.ceil(col_i / 3)
                #
                # row_range = range(self.get_row_start(cube_n), self.get_col_end(cube_n))
                # col_range = range(self.get_col_start(cube_n), self.get_col_end(cube_n))
                #
                # heuristic_values = [self.evaluate_list(puzzle[row]) for row in row_range]

        if not finished:
            return self.solve(initial_puzzle)

        print('Solved')
        print(puzzle)

        return puzzle

    def create_mask(self, puzzle):
        mask = puzzle.copy()
        mask[mask > 0] = 1

        return mask

    def fill_zero_values(self, puzzle):
        for cube_n in range(1,10):
            cube_values = self.get_cube_values(puzzle, cube_n)

            flatList = self.flatten_list(cube_values)

            random_number = list(range(1, 10))
            random.shuffle(random_number)

            for number in random_number:
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
