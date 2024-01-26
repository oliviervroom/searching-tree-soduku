import math
import sys
from src.ChronologicalBacktracking.ChronologicalBacktrackingWithForwardCheckingSolver import ChronologicalBacktrackingWithForwardCheckingSolver


#The class of the MCV algorithm
class ChronologicalBacktrackingWithForwardCheckingAndMostConstrainedVariable(ChronologicalBacktrackingWithForwardCheckingSolver):
    already_visited = []

    def solve(self, initial_values):
        # Init/Set already visited to empty.
        self.already_visited = []
        return super().solve(initial_values)

    def solve_element(self, element_n = 0):
        # Update stats.
        self.steps_forward = self.steps_forward + 1

        # If number of already visited fields + number of uneditable fields are
        # equal to 9*9, then we are done. Success!
        if (len(self.already_visited) + len(self.mask[self.mask == 1])) >= 9*9:
            return True

        # Init these variables to resolve coord of smallest domain.
        smallest_domain_size = math.inf
        smallest_domain_coord = None

        for (row, col), domain in self.domains.items():
            # If coord is not already visited and the domain is the smallest we
            # have seen, then set variables for smallest coord.
            if (row, col) not in self.already_visited and len(domain) < smallest_domain_size:
                smallest_domain_coord = (row, col)
                smallest_domain_size = len(domain)

        # Apply coords of smallest domain.
        (row, col) = smallest_domain_coord

        # Check coord as visited.
        self.already_visited.append((row, col))

        # Get domain of coord and loop over possible values.
        domain = self.get_domain(row, col)
        for value in domain:
            # Fill domain value in sudoku.
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
        # update related domains, pull out coord in already visited list, update
        # stats and return False so that above statement can go on in it's loop.
        self.sudoku.values[row][col] = 0
        self.already_visited.remove((row, col))
        self.update_domains(row, col)
        self.steps_backward = self.steps_backward + 1

        return False
