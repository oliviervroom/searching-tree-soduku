from src.SudokuGenerator import SudokuGenerator

fixed_values = list(range(17, 36))
fixed_values.reverse()

save_path = "./data/sample_data.txt"

fixed_values_to_get = {}
for n_fixed_values in fixed_values:
    if n_fixed_values in [17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]:
        continue

    fixed_values_to_get[n_fixed_values] = 10

file_path = "./data/puzzles3_magictour_top1465"

with open(file_path, 'r') as file:
    sudoku_inputs = file.read().splitlines()

for sudoku_input in sudoku_inputs:
    sudoku_grid = SudokuGenerator.parse_sudoku_input(sudoku_input)

    # Count non-zero numbers
    n_fixed_values = sum(1 for row in sudoku_grid for num in row if num != 0)

    if not n_fixed_values in fixed_values_to_get.keys():
        continue

    if fixed_values_to_get[n_fixed_values] > 0:
        with open(save_path, 'a') as file:
            file.write(sudoku_input + '\n')

        fixed_values_to_get[n_fixed_values] = fixed_values_to_get[n_fixed_values] - 1
        print(fixed_values_to_get)

    if sum(fixed_values_to_get) == 0:
        break