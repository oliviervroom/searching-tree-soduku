import math

from src.ChronologicalBacktracking.ChronologicalBacktrackingWithForwardCheckingSolver import ChronologicalBacktrackingWithForwardCheckingSolver


#The class of the algorithm
class ChronologicalBacktrackingWithForwardCheckingAndMostConstrainedVariable(ChronologicalBacktrackingWithForwardCheckingSolver):
    iteration = 0
    already_visited = []
    i = 0

    def solve_element(self, element_n = 0):
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

            if not self.is_valid(row, col, value):
                continue

            self.update_domains(row, col)

            if self.solve_element(element_n + 1):
                return True

            self.sudoku.values[row][col] = 0
            self.update_domains(row, col)

        self.already_visited.remove((row, col))
        self.update_domains(row, col)

        return False
