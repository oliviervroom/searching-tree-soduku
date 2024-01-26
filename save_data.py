from src.SudokuRepository import SudokuRepository

# This is the file were we picked out 10 samples per fixed value setting.
fixed_values = list(range(17, 36))
fixed_values.reverse()

# Were all sudokus were saved.
save_path = "./data/sample_data.txt"

# Controll over which setting we had to append to the file for testing.
fixed_values_to_get = {}
for n_fixed_values in fixed_values:
    if n_fixed_values in [17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]:
        continue

    fixed_values_to_get[n_fixed_values] = 10

# Set the file we had to obtain specific samples from.
file_path = "./data/puzzles3_magictour_top1465"

with open(file_path, 'r') as file:
    sudoku_inputs = file.read().splitlines()

for sudoku_input in sudoku_inputs:
    sudoku_grid = SudokuRepository.parse_sudoku_input(sudoku_input)

    # Count non-zero numbers
    n_fixed_values = sum(1 for row in sudoku_grid for num in row if num != 0)

    # skip if not found
    if not n_fixed_values in fixed_values_to_get.keys():
        continue

    # Found a setting that was still missing a sudoku
    if fixed_values_to_get[n_fixed_values] > 0:
        with open(save_path, 'a') as file:
            file.write(sudoku_input + '\n')

        fixed_values_to_get[n_fixed_values] = fixed_values_to_get[n_fixed_values] - 1
        print(fixed_values_to_get)

    # If 10 samples, then break.
    if sum(fixed_values_to_get) == 0:
        break