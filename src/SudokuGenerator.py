
class SudokuGenerator:

    @staticmethod
    def get_sudoku(requested_fixed_values):
        file_path = "./data/sample_data.txt"

        with open(file_path, 'r') as file:
            sudoku_inputs = file.read().splitlines()

        requested_sudokus = []
        for sudoku_input in sudoku_inputs:
            sudoku_grid = SudokuGenerator.parse_sudoku_input(sudoku_input)

            # Count non-zero numbers
            fixed_values = sum(1 for row in sudoku_grid for num in row if num != 0)
            if fixed_values == requested_fixed_values:
                requested_sudokus.append(sudoku_grid)

        return requested_sudokus

    @staticmethod
    def parse_sudoku_input(input_string):
        grid = [[0] * 9 for _ in range(9)]
        index = 0

        for row in range(9):
            for col in range(9):
                current_char = input_string[index]
                index += 1

                if current_char.isdigit():
                    grid[row][col] = int(current_char)
                elif current_char == '.':
                    grid[row][col] = 0

        return grid

