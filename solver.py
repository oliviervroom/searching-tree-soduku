import numpy as np
import math
import random
from enum import Enum
from SudokuState import SudokuState, LocalSearchState
from Sudoku import Sudoku
from SudokuHelper import SudokuHelper
import sys

#Class which decides to switch approach
class LocalSearchApproach(Enum):
    BEST_IMPROVEMENT = 0
    FIRST_IMPROVEMENT = 1

#The class of the algorithm
class Solver:
    finished = False
    verbose = False

    local_search_approach = LocalSearchApproach.FIRST_IMPROVEMENT

    n_of_switches = 0

    n_new_optimums = 0
    n_same_optimums = 0
    n_plateaus = 0
    n_patterns = 0
    n_random_walks = 0

    #Constructor method which takes parameters arguments (standard configuration is optimal)
    def __init__(self,
                 local_search_approach=LocalSearchApproach.FIRST_IMPROVEMENT,
                 optimization_credits=10,
                 random_credits=1,
                 pattern_credits=4,
                 plateau_credits=19,
                 max_tries=math.inf, verbose=True
                 ):
        self.optimization_credits = optimization_credits
        self.random_credits = random_credits
        self.pattern_credits = pattern_credits
        self.plateau_credits = plateau_credits
        self.max_tries = max_tries

        self.local_search_approach = local_search_approach

        #Initialise the row and column evaluations at 9
        self.row_evaluations = [9 for x in range(0, 9)]
        self.col_evaluations = [9 for x in range(0, 9)]

        self.verbose = verbose

    #The algorithm method which takes in a start situation
    def solve(self, initial_values):
        # 1. create mask for uneditable numbers
        self.mask = SudokuHelper.create_mask(initial_values)

        initial_values = np.array(initial_values)

        #Define our start situation to be a sudoku
        self.sudoku = Sudoku(initial_values)
        self.sudoku_state = SudokuState()

        # 2. for every cube fill numbers so that we have numbers 1-9
        self.sudoku.fill_zero_values()

        # 3. Calculate the evaluation of all rows and columns based on the randomly filled-in sudoku
        self.update_evaluation()

        tries = 0
        best_eval = math.inf

        # 4. Loop over the sudoku 
        while True:
            tries += 1

            if tries > self.max_tries:
                break

            #Save the current evaluations of all rows and columns
            current_eval = sum(self.row_evaluations) + sum(self.col_evaluations)

            #If the current sudoku evaluations is zero, stop the loop
            if current_eval == 0:
                self.finished = True
                break

            #Pick a random cube
            cube_n = random.randint(1, 9)

            #Perform local search on the cube and assign a state when finished
            local_state = self.local_search(cube_n, self.optimization_credits, self.plateau_credits,
                                            self.pattern_credits)

            self.sudoku_state.update_cube(cube_n, local_state)

            #Sum all none and new_optimum states
            sum_of_none = self.sudoku_state.number_of_nones()
            sum_of_new_optimums = self.sudoku_state.number_of_new_optimums()

            #Perform a random walk when there are no none and new_optimum states
            if sum_of_new_optimums == 0 and sum_of_none == 0:
                self.n_random_walks += 1
                for x in range(0, self.random_credits):
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
                        end = SudokuHelper.get_absolute_end(start, end_switch_i)

                        if self.mask[end[0]][end[1]] == 0 and not start == end:
                            self.sudoku.switch(start, end)

                            rows = list({start[0], end[0]})
                            cols = list({start[1], end[1]})

                            self.n_of_switches += 1

                            self.update_evaluation(rows, cols)

                            break

                self.sudoku_state.reset()

            # logging the state
            if local_state == LocalSearchState.NEW_OPTIMUM:
                self.n_new_optimums += 1

            if local_state == LocalSearchState.SAME_OPTIMUM:
                self.n_same_optimums += 1

            if local_state == LocalSearchState.PLATEAU:
                self.n_plateaus += 1

            if local_state == LocalSearchState.PATTERN:
                self.n_patterns += 1

            #show a live log when solving a sudoku
            if self.verbose:
                sum_of_new_optimums = self.sudoku_state.number_of_new_optimums()
                sum_of_same_optimums = self.sudoku_state.number_of_same_optimums()
                sum_of_plateaus = self.sudoku_state.number_of_plateaus()
                sum_of_patterns = self.sudoku_state.number_of_patterns()
                sum_of_none = self.sudoku_state.number_of_nones()

                if current_eval < best_eval:
                    best_eval = current_eval

                if tries % 1000 == 0:
                    sys.stdout.write(
                        f"\rswitches: {self.n_of_switches}, "
                        f"best_eval: {best_eval}, "
                        f"current_eval: {current_eval}, "
                        f"new_optimums: {sum_of_new_optimums}, "
                        f"same_optimums: {sum_of_same_optimums}, "
                        f"patterns: {sum_of_patterns}, "
                        f"plateaus: {sum_of_plateaus}, "
                        f"nones: {sum_of_none}"
                    )
                    sys.stdout.flush()

        if self.verbose:
            if tries > 1000:
                print('')

            print('Finished.')

        return self.sudoku.values

    #The local search algorithm
    def local_search(self, cube_n, optimization_credits=10, plateau_credits=5, pattern_credits=5):
        pattern_credits = pattern_credits + plateau_credits

        with_optimization_credits = optimization_credits > 0
        with_pattern_detection = pattern_credits > 0
        with_plateau_detection = plateau_credits > 0

        #Set all evaluations when starting local search in a cube
        starting_eval_sum = sum(self.row_evaluations) + sum(self.col_evaluations)
        last_eval_sum = starting_eval_sum
        last_states = [self.sudoku.values]

        #Loop over the cube
        while True:
            #Pick a random start entry
            start = SudokuHelper.random_entry(cube_n, lambda position: self.mask[position[0]][position[1]] == 0)

            random_end_ints = list(range(0, 9))
            random.shuffle(random_end_ints)
            switched = False

            #First-improvement approach
            if self.local_search_approach == LocalSearchApproach.FIRST_IMPROVEMENT:
                
                #Loop over each end entry in the cube
                for random_end_i in random_end_ints:
                    end = SudokuHelper.get_absolute_end(start, random_end_i)

                    if self.mask[end[0]][end[1]] == 0 and not start == end:
                        rows = list({start[0], end[0]})
                        cols = list({start[1], end[1]})

                        old_eval = sum(self.evaluate(rows=rows, cols=cols))
                        self.sudoku.switch(start, end)
                        new_eval = sum(self.evaluate(rows=rows, cols=cols))

                        #Switch as soon as you find an improvement in evaluations
                        if new_eval <= old_eval:
                            rows = list({start[0], end[0]})
                            cols = list({start[1], end[1]})

                            self.update_evaluation(rows, cols)

                            self.n_of_switches += 1

                            switched = True

                            break
                        else:
                            self.sudoku.switch(end, start)

            #Best-improvement approach
            elif self.local_search_approach == LocalSearchApproach.BEST_IMPROVEMENT:
                evals_after_switch = {}

                #Loop over each end entry in the cube
                for random_end_i in random_end_ints:
                    end = SudokuHelper.get_absolute_end(start, random_end_i)

                    if self.mask[end[0]][end[1]] == 0 and not start == end:
                        rows = list({start[0], end[0]})
                        cols = list({start[1], end[1]})

                        old_eval = sum(self.evaluate(rows=rows, cols=cols))
                        self.sudoku.switch(start, end)
                        new_eval = sum(self.evaluate(rows=rows, cols=cols))
                        self.sudoku.switch(end, start)

                        if new_eval <= old_eval:
                            evals_after_switch[old_eval - new_eval] = end
                
                #Store all improvements in a dictionairy
                eval_wins = evals_after_switch.keys()

                if len(eval_wins) == 0:
                    break

                best_eval_win = max(eval_wins)

                if best_eval_win not in evals_after_switch:
                    break
                    
                #Pick the best evaluation improvement and perform the associated switch
                end = evals_after_switch[best_eval_win]

                self.sudoku.switch(start, end)

                rows = list({start[0], end[0]})
                cols = list({start[1], end[1]})

                self.update_evaluation(rows, cols)

                self.n_of_switches += 1

                switched = True

            current_eval_sum = sum(self.row_evaluations) + sum(self.col_evaluations)

            #Deduct credits when:
            #-A switch was performed which improved the evaluation
            if with_optimization_credits:
                if with_plateau_detection and current_eval_sum < starting_eval_sum or not with_plateau_detection and current_eval_sum <= starting_eval_sum:
                    optimization_credits -= 1
                    
                #Return an optimum state
                if optimization_credits <= 0:
                    if starting_eval_sum == current_eval_sum:
                        return LocalSearchState.SAME_OPTIMUM
                    else:
                        return LocalSearchState.NEW_OPTIMUM

            #No switch was performed or the current evaluation is zero
            if not switched or current_eval_sum == 0:
                if starting_eval_sum == current_eval_sum:
                    return LocalSearchState.SAME_OPTIMUM
                else:
                    return LocalSearchState.NEW_OPTIMUM
            
            #Is the new state not in the taboo list of previous states
            if with_pattern_detection:
                new_state = not any(np.array_equal(self.sudoku.values, arr) for arr in last_states)

                #If it is in the taboo list of previous states, deduct a credit
                if not new_state:
                    pattern_credits -= 1

                #If credits are spend
                if pattern_credits <= 0:
                    return LocalSearchState.PATTERN

            #If the cube end with the same evaluations, deduct a plateau credit
            if with_plateau_detection and last_eval_sum == current_eval_sum:
                plateau_credits -= 1

                #If credits are spend
                if plateau_credits <= 0:
                    return LocalSearchState.PLATEAU

            last_eval_sum = sum(self.row_evaluations) + sum(self.col_evaluations)

    #This function updates all evaluations of the selected rows and columns
    def update_evaluation(self, rows=None, cols=None):
        if rows is None:
            rows = range(0, 9)

        if cols is None:
            cols = range(0, 9)

        for row, eval in zip(rows, self.evaluate(rows=rows)):
            self.row_evaluations[row] = eval

        for col, eval in zip(cols, self.evaluate(cols=cols)):
            self.col_evaluations[col] = eval

    #This function evaluated rows and columns
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
    
    #This function uses our self defined heuristic to determine the heuristic value of a row/column
    def evaluate_list(self, list):
        return int(9 - len(set(list)))
