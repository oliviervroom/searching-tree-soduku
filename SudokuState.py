from enum import Enum


class LocalSearchState(Enum):
    NONE = 0
    PLATEAU = 1
    PATTERN = 2
    SAME_OPTIMUM = 3
    NEW_OPTIMUM = 4


class SudokuState:
    states = {
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

    def number_of_nones(self):
        return self.number_of(LocalSearchState.NONE)

    def number_of_plateaus(self):
        return self.number_of(LocalSearchState.PLATEAU)

    def number_of_same_optimums(self):
        return self.number_of(LocalSearchState.SAME_OPTIMUM)

    def number_of_new_optimums(self):
        return self.number_of(LocalSearchState.NEW_OPTIMUM)

    def number_of(self, state):
        return sum([s is state for s in self.states.values()])

    def update_cube(self, cube_n, state):
        self.states[cube_n] = state

    def reset(self):
        for n in range(1, 10):
            self.states[n] = LocalSearchState.NONE