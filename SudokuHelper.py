import math
import random
import numpy

class SudokuHelper:

    @staticmethod
    def create_mask(values):
        mask = numpy.array(values)
        mask[mask > 0] = 1

        return mask

    @staticmethod
    def fill_zero_values(values):
        for cube_n in range(1, 10):
            cube_values = SudokuHelper.get_cube_values(values, cube_n)

            flat_list = [item for sublist in cube_values for item in sublist]

            random_number = list(range(1, 10))
            random.shuffle(random_number)

            for number in random_number:
                if number not in flat_list:
                    for i, value in enumerate(flat_list):
                        if value == 0:
                            flat_list[i] = number
                            break

            values[
                SudokuHelper.get_row_start(cube_n):SudokuHelper.get_row_end(cube_n),
                SudokuHelper.get_col_start(cube_n):SudokuHelper.get_col_end(cube_n)
            ] = [flat_list[i:i + 3] for i in range(0, len(flat_list), 3)]

        return values

    @staticmethod
    def random_entry(cube_n, test):
        random_entry_ints = list(range(0, 9))
        random.shuffle(random_entry_ints)

        for random_entry_i in random_entry_ints:
            pos = SudokuHelper.get_absolute_end((SudokuHelper.get_row_start(cube_n), SudokuHelper.get_col_start(cube_n)), random_entry_i)

            if test(pos):
                return pos

    @staticmethod
    def get_absolute_end(start, end_switch_i):
        cube_row_base = ((math.ceil((start[0] + 1) / 3) - 1) * 3)
        cube_col_base = ((math.ceil((start[1] + 1) / 3) - 1) * 3)
        end_switch_row = cube_row_base + math.ceil((end_switch_i + 1) / 3) - 1
        end_switch_col = cube_col_base + end_switch_i % 3

        return (end_switch_row, end_switch_col)

    @staticmethod
    def get_col_start(cube):
        return int(((cube - 1) % 3) * 3)

    @staticmethod
    def get_col_end(cube):
        return int(((cube - 1) % 3) * 3 + 3)

    @staticmethod
    def get_row_start(cube):
        return int((math.ceil(cube / 3) - 1) * 3)

    @staticmethod
    def get_row_end(cube):
        return int((math.ceil(cube / 3) - 1) * 3 + 3)

    @staticmethod
    def get_cube_values(puzzle, cube_n):
        return puzzle[
           SudokuHelper.get_row_start(cube_n):SudokuHelper.get_row_end(cube_n),
           SudokuHelper.get_col_start(cube_n):SudokuHelper.get_col_end(cube_n)
       ]