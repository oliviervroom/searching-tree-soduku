import numpy as np
import math
import random
from SudokuState import SudokuState, LocalSearchState
from Sudoku import Sudoku
import sys


class Solver:
    finished = False
    switches = 0

    n_new_optimums = 0
    n_same_optimums = 0
    n_plateaus = 0
    n_patterns = 0
    n_random_walks = 0

    def __init__(self, optimization_credits=10, random_credits=2, pattern_credits=15, plateau_credits=20,
                 max_tries=math.inf):
        self.optimization_credits = optimization_credits
        self.random_credits = random_credits
        self.pattern_credits = pattern_credits
        self.plateau_credits = plateau_credits
        self.max_tries = max_tries

    def solve(self, initial_values):
        # 1. create mask for uneditable numbers
        self.mask = self.create_mask(initial_values)

        initial_values = np.array(initial_values)

        # 2. for every cube fill numbers so that we have numbers 1-9
        self.sudoku = Sudoku(self.fill_zero_values(initial_values))
        self.sudoku_state = SudokuState()

        # 3. Calculate the evaluation of all rows and columns based on the randomly filled-in sudoku
        self.row_evaluations = [self.evaluate_list(row) for row in self.sudoku.values[0:9, :]]
        self.col_evaluations = [self.evaluate_list(col) for col in self.sudoku.values[:, 0:9]]

        # 4. Locate the cube with the highest evaluated entry and switch within the cube to obtain 
        # a lower evaluation for the affected rows and columns
        # TODO Moet de switch binnen een lokaal de eerste verbetering doen of de beste verbetering opzoeken
        # TODO Zodra een switch is gedaan, moet er dan naar een andere waarde in het lokaal worden gekeken
        # of bekijken we dan de hoogste evaluatie van de hele sudoku

        tries = 0
        best_eval = math.inf

        while True:
            tries += 1

            if tries > self.max_tries:
                break

            highest_row_eval = max(self.row_evaluations)
            highest_col_eval = max(self.col_evaluations)

            current_eval = highest_row_eval + highest_col_eval

            if current_eval == 0:
                self.finished = True
                break

            cube_n = random.randint(1, 9)

            local_state = self.local_search(cube_n, self.optimization_credits, self.plateau_credits,
                                            self.pattern_credits)

            if local_state == LocalSearchState.NEW_OPTIMUM:
                self.n_new_optimums += 1

            if local_state == LocalSearchState.SAME_OPTIMUM:
                self.n_same_optimums += 1

            if local_state == LocalSearchState.PLATEAU:
                self.n_plateaus += 1

            if local_state == LocalSearchState.PATTERN:
                self.n_patterns += 1

            self.sudoku_state.update_cube(cube_n, local_state)

            sum_of_none = self.sudoku_state.number_of_nones()
            sum_of_new_optimums = self.sudoku_state.number_of_new_optimums()

            if sum_of_new_optimums == 0 and sum_of_none == 0:
                self.n_random_walks += 1
                for x in range(0, max(1, current_eval)):
                    start = None

                    while True:
                        pos = (random.randint(0, 8), random.randint(0, 8))

                        if self.mask[pos[0]][pos[1]] == 0:
                            start = pos
                            break

                    if start is None:
                        break

                    random_switches = list(range(0, 8))
                    random.shuffle(random_switches)

                    for end_switch_i in random_switches:
                        end = self.get_absolute_end(start, end_switch_i)

                        if self.mask[end[0]][end[1]] == 0 and not self.is_locked(start, end):
                            self.sudoku.switch(start, end)

                            rows = list({start[0], end[0]})
                            cols = list({start[1], end[1]})

                            self.switches += 1

                            self.update_evaluation(rows, cols)

                            break

                self.sudoku_state.reset()

            # sum_of_new_optimums = self.sudoku_state.number_of_new_optimums()
            # sum_of_same_optimums = self.sudoku_state.number_of_same_optimums()
            # sum_of_plateaus = self.sudoku_state.number_of_plateaus()
            #
            # if current_eval < best_eval:
            #     best_eval = current_eval
            #
            # if tries % 1000 == 0:
            #     sys.stdout.write(f"\rtries: {tries}, Best eval: {best_eval}, current_eval: {current_eval}, new_optimums: {sum_of_new_optimums}, same_optimums: {sum_of_same_optimums}, plateaus: {sum_of_plateaus}")
            #     sys.stdout.flush()

        return self.sudoku.values

    def create_mask(self, values):
        mask = np.array(values)
        mask[mask > 0] = 1

        return mask

    def fill_zero_values(self, values):
        for cube_n in range(1, 10):
            cube_values = self.get_cube_values(values, cube_n)

            flat_list = self.flatten_list(cube_values)

            random_number = list(range(1, 10))
            random.shuffle(random_number)

            for number in random_number:
                if number not in flat_list:
                    for i, value in enumerate(flat_list):
                        if value == 0:
                            flat_list[i] = number
                            break

            values[self.get_row_start(cube_n):self.get_row_end(cube_n),
            self.get_col_start(cube_n):self.get_col_end(cube_n)] = [flat_list[i:i + 3] for i in
                                                                    range(0, len(flat_list), 3)]

        return values

    def local_search(self, cube_n, optimization_credits=10, plateau_credits=5, pattern_credits=5):
        pattern_credits = pattern_credits + plateau_credits

        with_optimization_credits = optimization_credits > 0
        with_pattern_detection = pattern_credits > 0
        with_plateau_detection = plateau_credits > 0

        starting_eval_sum = sum(self.row_evaluations) + sum(self.col_evaluations)
        last_eval_sum = starting_eval_sum
        last_states = [self.sudoku.values]

        while True:
            start = self.random_entry(cube_n, lambda position: self.mask[position[0]][position[1]] == 0)

            random_end_ints = list(range(0, 9))
            random.shuffle(random_end_ints)
            switched = False

            for random_end_i in random_end_ints:
                end = self.get_absolute_end(start, random_end_i)

                if self.mask[end[0]][end[1]] == 0 and not start == end:
                    rows = list({start[0], end[0]})
                    cols = list({start[1], end[1]})

                    old_eval = sum(self.evaluate(rows=rows, cols=cols))
                    self.sudoku.switch(start, end)
                    new_eval = sum(self.evaluate(rows=rows, cols=cols))

                    if new_eval <= old_eval:
                        rows = list({start[0], end[0]})
                        cols = list({start[1], end[1]})

                        self.update_evaluation(rows, cols)

                        self.switches += 1

                        switched = True
                    else:
                        self.sudoku.switch(end, start)

            current_eval_sum = sum(self.row_evaluations) + sum(self.col_evaluations)

            if with_optimization_credits:
                if with_plateau_detection and current_eval_sum < starting_eval_sum or not with_plateau_detection and current_eval_sum <= starting_eval_sum:
                    optimization_credits -= 1

                if optimization_credits <= 0:
                    if starting_eval_sum == current_eval_sum:
                        return LocalSearchState.SAME_OPTIMUM
                    else:
                        return LocalSearchState.NEW_OPTIMUM

            if not switched or current_eval_sum == 0:
                if starting_eval_sum == current_eval_sum:
                    return LocalSearchState.SAME_OPTIMUM
                else:
                    return LocalSearchState.NEW_OPTIMUM

            if with_pattern_detection:
                new_state = not any(np.array_equal(self.sudoku.values, arr) for arr in last_states)

                if not new_state:
                    pattern_credits -= 1

                if pattern_credits <= 0:
                    return LocalSearchState.PATTERN

            if with_plateau_detection and last_eval_sum == current_eval_sum:
                plateau_credits -= 1

                if plateau_credits <= 0:
                    return LocalSearchState.PLATEAU

            last_eval_sum = sum(self.row_evaluations) + sum(self.col_evaluations)

    def random_entry(self, cube_n, test):
        random_entry_ints = list(range(0, 9))
        random.shuffle(random_entry_ints)

        for random_entry_i in random_entry_ints:
            pos = self.get_absolute_end((self.get_row_start(cube_n), self.get_col_start(cube_n)), random_entry_i)

            if test(pos):
                return pos

    def get_absolute_end(self, start, end_switch_i):
        cube_row_base = ((math.ceil((start[0] + 1) / 3) - 1) * 3)
        cube_col_base = ((math.ceil((start[1] + 1) / 3) - 1) * 3)
        end_switch_row = cube_row_base + math.ceil((end_switch_i + 1) / 3) - 1
        end_switch_col = cube_col_base + end_switch_i % 3

        return (end_switch_row, end_switch_col)

    def is_locked(self, start, end):
        return start == end

    def update_evaluation(self, rows, cols):
        for row, eval in zip(rows, self.evaluate(rows=rows)):
            self.row_evaluations[row] = eval

        for col, eval in zip(cols, self.evaluate(cols=cols)):
            self.col_evaluations[col] = eval

    def virtual_switch(self, start, end):
        virtual = self.sudoku.values.copy()

        # get values
        start_value = virtual[start[0]][start[1]]
        end_value = virtual[end[0]][end[1]]

        # switch values
        virtual[start[0]][start[1]] = end_value
        virtual[end[0]][end[1]] = start_value

        return virtual

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

    def evaluate(self, rows=None, cols=None):
        if rows is None and cols is None:
            rows = range(0, 9)
            cols = range(0, 9)

        lists = []

        if cols is not None:
            for col in cols:
                lists.extend([self.sudoku.values[:, col]])

        if rows is not None:
            for row in rows:
                lists.extend([self.sudoku.values[row, :]])

        return [self.evaluate_list(col_or_list) for col_or_list in lists]

    def evaluate_list(self, list):
        return int(9 - len(set(list)))

    def wrong_entries(self):
        wrong_entries = 0

        for puzzle_row, solution_row in zip(self.sudoku.values, self.solution):
            for puzzle_entry, solution_entry in zip(puzzle_row, solution_row):
                if puzzle_entry != solution_entry:
                    wrong_entries += 1

        return wrong_entries

    def default_sudoku_state(self):
        return {
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
