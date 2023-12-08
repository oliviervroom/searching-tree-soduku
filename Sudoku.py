import math

class Sudoku:
    def __init__(self, values):
        self.values = values

    def switch(self, a, b):
        # get values
        start_value = self.values[a[0]][a[1]]
        end_value = self.values[b[0]][b[1]]

        # switch values
        self.values[a[0]][a[1]] = end_value
        self.values[b[0]][b[1]] = start_value

    def get_cube_values(self, puzzle, cube_n):
        return puzzle[
           self.get_row_start_by_cube(cube_n):self.get_row_end_by_cube(cube_n),
           self.get_col_start_by_cube(cube_n):self.get_col_end_by_cube(cube_n)
       ]

    def get_col_start_by_cube(self, cube):
        return int(((cube - 1) % 3) * 3)

    def get_col_end_by_cube(self, cube):
        return int(((cube - 1) % 3) * 3 + 3)

    def get_row_start_by_cube(self, cube):
        return int((math.ceil(cube / 3) - 1) * 3)

    def get_row_end_by_cube(self, cube):
        return int((math.ceil(cube / 3) - 1) * 3 + 3)