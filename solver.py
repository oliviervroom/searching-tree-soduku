import numpy as np
import math
import random
from enum import Enum
import sys

class LocalSearchState(Enum):
    NONE = 0
    PLATEAU = 1
    SAME_OPTIMUM = 2
    NEW_OPTIMUM = 3

class Solver:

    def __init__(self, initial_puzzle):
        self.alg_tries = 0
        self.initial_puzzle = initial_puzzle

        self.init()

    def init(self):
        self.puzzle = np.array(self.initial_puzzle)

        # 1. create mask for uneditable numbers
        self.mask = self.create_mask(self.puzzle)

        # 2. for every cube fill numbers so that we have numbers 1-9
        # TODO verander de functie zodat de nummers eerst geshuffeld worden voordat ze iteratief de nullen vervangen.
        self.puzzle = self.fill_zero_values(self.puzzle)

        # 3. Calculate the evaluation of all rows and columns based on the randomly filled-in sudoku

        self.row_evaluations = [self.evaluate_list(self.puzzle[row]) for row in range(0, 9)]
        self.col_evaluations = [self.evaluate_list(self.flatten_list(self.puzzle[0:9, col:col + 1])) for col in range(0, 9)]

    def solve(self):
        # 4. Locate the cube with the highest evaluated entry and switch within the cube to obtain 
        # a lower evaluation for the affected rows and columns
        #TODO Moet de switch binnen een lokaal de eerste verbetering doen of de beste verbetering opzoeken
        #TODO Zodra een switch is gedaan, moet er dan naar een andere waarde in het lokaal worden gekeken
        # of bekijken we dan de hoogste evaluatie van de hele sudoku

        finished = False

        self.alg_tries += 1

        print('Tries:', self.alg_tries)

        tries = 0
        best_eval = 99999

        random_credits = 2
        pattern_credits = 5
        plateau_credits = 10

        cube_states = {
            1: LocalSearchState.NONE,
            2: LocalSearchState.NONE,
            3: LocalSearchState.NONE,
            4: LocalSearchState.NONE,
            5: LocalSearchState.NONE,
            6: LocalSearchState.NONE,
            7: LocalSearchState.NONE,
            8: LocalSearchState.NONE,
            9: LocalSearchState.NONE
        }

        while not finished:
            tries += 1

            highest_row_eval = max(self.row_evaluations)
            highest_col_eval = max(self.col_evaluations)

            current_eval = sum(self.row_evaluations) + sum(self.col_evaluations)

            sum_of_new_optimums = sum(state is LocalSearchState.NEW_OPTIMUM for state in cube_states.values())
            sum_of_same_optimums = sum(state is LocalSearchState.SAME_OPTIMUM for state in cube_states.values())
            sum_of_plateaus = sum(state is LocalSearchState.PLATEAU for state in cube_states.values())

            if tries % 1000 == 0:
                sys.stdout.write(f"\rtries: {tries}, current_eval: {current_eval}, new_optimums: {sum_of_new_optimums}, same_optimums: {sum_of_same_optimums}, plateaus: {sum_of_plateaus}")
                sys.stdout.flush()

            if current_eval < best_eval:
                best_eval = current_eval
                print(f"\nTries: {tries}\nNew best eval: {best_eval}\nCurrent sudoku:\n{self.puzzle}\n")

            if (highest_row_eval + highest_col_eval) == 0:
                finished = True
                break

            # row_i = row_evaluations.index(highest_row_eval)
            # col_i = col_evaluations.index(highest_col_eval)

            #cube_n = 1 + (math.floor(row_i/3) * 3) + math.floor(col_i / 3)
            cube_n = random.randint(1,9)

            # print('Cube:', cube_n)

            highest_local_row_eval = max(self.row_evaluations[self.get_row_start(cube_n):self.get_row_end(cube_n)])
            highest_local_col_eval = max(self.col_evaluations[self.get_col_start(cube_n):self.get_col_end(cube_n)])

            start_row = ((math.ceil(cube_n / 3) - 1) * 3) + self.row_evaluations[self.get_row_start(cube_n):self.get_row_end(cube_n)].index(highest_local_row_eval)
            start_col = (math.floor((cube_n - 1) % 3) + 1) + self.col_evaluations[self.get_col_start(cube_n):self.get_col_end(cube_n)].index(highest_local_col_eval)

            start = (start_row, start_col)

            cube_states[cube_n] = self.local_search(start, plateau_credits, pattern_credits)

            # print('Randomizing. Number of new optimums:', sum_of_new_optimums, current_eval)
            if sum_of_new_optimums == 0:
                for x in range(1, random_credits):
                    random_start = (random.randint(0,8), random.randint(0,8))
                    random_switches = list(range(0, 8))
                    random.shuffle(random_switches)

                    for end_switch_i in random_switches:
                        end = self.get_absolute_end(random_start, end_switch_i)

                        if self.mask[end[0]][end[1]] == 0 and not self.is_locked(random_start, end):
                            virtual = self.virtual_switch(random_start, end)
                            self.puzzle = virtual

            # print('Start switch:', start_switch_row, start_switch_col)

            # if highest_local_row_eval > highest_local_col_eval:
            #     is_locked = lambda row, col: row == start_switch_row
            # else:
            #     is_locked = lambda row, col: col == start_switch_col

        if not finished:
            self.init()
            return self.solve()

        print('Solved')
        print(self.puzzle)

        return self.puzzle

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

    def local_search(self, start, plateau_credits=5, pattern_credits=5):
        plateau_credits = pattern_credits + plateau_credits

        starting_eval_sum = sum(self.row_evaluations) + sum(self.col_evaluations)
        last_eval_sum = starting_eval_sum
        switch_tries = 0
        # last_switch = None
        last_states = [self.puzzle]
        while True:
            # tried_same_switch = False
            random_switches = list(range(0, 8))
            random.shuffle(random_switches)

            switched = False

            for end_switch_i in random_switches:
                end = self.get_absolute_end(start, end_switch_i)
                switch = (start, end)

                # tried_same_switch = switch == last_switch

                if self.mask[end[0]][end[1]] == 0 and not self.is_locked(start, end):
                    virtual = self.virtual_switch(start, end)

                    rows = list({start[0], end[0]})
                    cols = list({start[1], end[1]})

                    old_rows_eval = sum([self.evaluate_list(row) for row in self.puzzle[rows]])
                    old_cols_eval = sum([self.evaluate_list([self.puzzle[row, col] for row in range(0, 9)]) for col in cols])

                    new_row_evals = [self.evaluate_list(row) for row in virtual[rows]]
                    new_rows_eval = sum(new_row_evals)
                    new_col_evals = [self.evaluate_list([virtual[row, col] for row in range(0, 9)]) for col in cols]
                    new_cols_eval = sum(new_col_evals)

                    new_state = not any(np.array_equal(virtual, arr) for arr in last_states)

                    if not new_state:
                        pattern_credits -= 1

                    if (new_rows_eval + new_cols_eval) <= (old_rows_eval + old_cols_eval):
                        self.puzzle = virtual

                        last_states.append(self.puzzle)

                        for row, eval in zip(rows, new_row_evals):
                            self.row_evaluations[row] = eval

                        for col, eval in zip(cols, new_col_evals):
                            self.col_evaluations[col] = eval

                        switched = True
                        # last_switch = switch

                        break

            current_eval_sum = sum(self.row_evaluations) + sum(self.col_evaluations)

            # if tried_same_switch and not switched:
            #     return LocalSearchState.PLATEAU

            if not switched or current_eval_sum == 0:
                # optimum
                # print('optimum', current_eval)
                if starting_eval_sum == current_eval_sum:
                    return LocalSearchState.SAME_OPTIMUM
                else:
                    return LocalSearchState.NEW_OPTIMUM

            if pattern_credits <= 0:
                return LocalSearchState.PLATEAU

            if last_eval_sum <= current_eval_sum:
                # plateau
                switch_tries += 1

                if switch_tries > plateau_credits:
                    return LocalSearchState.PLATEAU

            last_eval_sum = sum(self.row_evaluations) + sum(self.col_evaluations)
            start = self.get_absolute_end(start, random.randint(0, 8))

    def get_absolute_end(self, start, end_switch_i):
        cube_row_base = ((math.ceil((start[0] + 1) / 3) - 1) * 3)
        cube_col_base = ((math.ceil((start[1] + 1) / 3) - 1) * 3)
        end_switch_row = cube_row_base + math.ceil((end_switch_i + 1) / 3) - 1
        end_switch_col = cube_col_base + end_switch_i % 3

        return (end_switch_row, end_switch_col)

    def is_locked(self, start, end):
        return start == end

    def virtual_switch(self, start, end):
        virtual = self.puzzle.copy()

        # get values
        start_value = virtual[start[0]][start[1]]
        end_value = virtual[end[0]][end[1]]

        # switch values
        virtual[start[0]][start[1]] = end_value
        virtual[end[0]][end[1]] = start_value

        return virtual

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
