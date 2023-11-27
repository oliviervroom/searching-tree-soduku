import tkinter as tk
from tkinter import messagebox

class Renderer:
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def print(self):
        for row in self.puzzle:
            print("\t".join(str(num) if num != 0 else "." for num in row))

    def render(self):
        root = tk.Tk()
        root.title("Sudoku Game")

        for y, row in enumerate(self.puzzle):
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
        #     # For now, it just updates the puzzle array
        #     self.puzzle[y][x] = new_value
        # except ValueError:
        #     messagebox.showerror("Invalid Input", "Please enter a number between 1 and 9")
        #     event.widget.delete(0, tk.END)
        #     event.widget.insert(0, str(self.puzzle[y][x]) if self.puzzle[y][x] != 0 else "")

