
def main():
    file_path = "path/to/your/file.txt"  

    with open(file_path, 'r') as file:
        sudoku_inputs = file.read().splitlines()

    for input_string in sudoku_inputs:
        sudoku_grid = parse_sudoku_input(input_string)

        # Count non-zero numbers
        non_zero_count = sum(1 for row in sudoku_grid for num in row if num != 0)
        print(f"Number of non-zero numbers: {non_zero_count}")

        print_sudoku(sudoku_grid)
        print()  # Add a newline between Sudoku grids

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

def print_sudoku(grid):
    for row in grid:
        print(" ".join(map(str, row)))

if __name__ == "__main__":
    main()
