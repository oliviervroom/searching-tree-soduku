import math
import sys
from src.ChronologicalBacktracking.ChronologicalBacktrackingWithForwardCheckingSolver import ChronologicalBacktrackingWithForwardCheckingSolver


#The class of the algorithm
class ChronologicalBacktrackingWithForwardCheckingAndMostConstrainedVariable(ChronologicalBacktrackingWithForwardCheckingSolver):
    already_visited = []

    def solve(self, initial_values):
        self.already_visited = []
        return super().solve(initial_values)

    def solve_element(self, element_n = 0):
        self.steps_forward = self.steps_forward + 1

        if (len(self.already_visited) + len(self.mask[self.mask == 1])) >= 9*9:
            return True

        smallest_domain_size = math.inf
        smallest_domain_coord = None

        for (row, col), domain in self.domains.items():
            if (row, col) not in self.already_visited and len(domain) < smallest_domain_size:
                smallest_domain_coord = (row, col)
                smallest_domain_size = len(domain)

        (row, col) = smallest_domain_coord

        self.already_visited.append((row, col))

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
        self.already_visited.remove((row, col))
        self.update_domains(row, col)
        self.steps_backward = self.steps_backward + 1

        return False
