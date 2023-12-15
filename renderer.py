import tkinter as tk
from tkinter import messagebox

class Renderer:
    def __init__(self, sudoku):
        self.sudoku = sudoku

    def print(self):
        print()
        if not all(len(row) == 9 for row in self.sudoku) or len(self.sudoku) != 9:
            print("Invalid Sudoku: It must be a 9x9 grid.")
            return

            # Iterate through each row in the Sudoku
        for i, row in enumerate(self.sudoku):
            # Print a horizontal line every 3 rows
            if i % 3 == 0:
                if i == 0:
                    print("* ----- Result :) ----- *")
                else:
                    print("| --------------------- |")

            # Iterate through each number in the row
            for j, num in enumerate(row):
                # Print a vertical line every 3 columns
                if j % 3 == 0 and j != 0:
                    print("| ", end="")

                # Print the number
                if j == 0:  # Move to the next line after the last number
                    print("| " + str(num), end=" ")
                elif j == 8:  # Move to the next line after the last number
                    print(str(num) + " |")
                else:  # Stay on the same line
                    print(str(num) + " ", end="")

        print("* --------------------- *")

    def render(self):
        root = tk.Tk()
        root.title("Sudoku Game")

        for y, row in enumerate(self.sudoku):
            for x, num in enumerate(row):
                e = tk.Entry(root, width=2, font=('Arial', 24), justify='center')
                e.grid(row=y, column=x, stick="nsew", padx=1, pady=1)
                e.insert(0, str(num) if num != 0 else "")
                e.bind('<FocusOut>', lambda event, x=x, y=y: self.on_cell_entry(event, x, y))

        root.mainloop()

    def on_cell_entry(self, event, x, y):
        """ Handle cell value change event """
        # try:
        #     new_value = int(event.widget.get())
        #     if event.widget.get() is not None and (new_value < 1 or new_value > 9):
        #         raise ValueError
        #     # Here you can add logic to check if the new value is correct
        #     # For now, it just updates the sudoku array
        #     self.sudoku[y][x] = new_value
        # except ValueError:
        #     messagebox.showerror("Invalid Input", "Please enter a number between 1 and 9")
        #     event.widget.delete(0, tk.END)
        #     event.widget.insert(0, str(self.sudoku[y][x]) if self.sudoku[y][x] != 0 else "")

