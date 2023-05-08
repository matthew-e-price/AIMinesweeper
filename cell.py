from tkinter import *
from PIL import Image, ImageTk
import random
import settings
import ctypes
import sys


class Cell:
    all_cells = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None

    # Initializer
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.cell_btn_object = None
        self.x = x
        self.y = y
        self.surrounding_mines = 0
        self.is_revealed = False
        self.is_flagged = False

        self.img = (Image.open("Images/MineDefault.png"))
        self.img = self.img.resize((50, 50), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)

        Cell.all_cells.append(self)

    # Creates a button object for this cell
    def create_btn_object(self, location):
        btn = Button(
            location,
            width=50,
            height=50,
            borderwidth=0,
            image=self.img
        )
        btn.bind("<Button-1>", self.handle_left_click)
        btn.bind("<Button-3>", self.handle_right_click)
        self.cell_btn_object = btn

    # Action on left click, used to reveal cells
    def handle_left_click(self, event):
        if self.is_mine and not self.is_flagged:
            self.show_mine()
        elif not self.is_flagged:
            self.show_cell()
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(0, "Congratulations! You win!", "Game Over", 0)
                sys.exit()

    # Action on right click, used to flag cells
    def handle_right_click(self, event):
        if not self.is_flagged and not self.is_revealed:
            self.cell_btn_object.configure(bg="blue")
            self.is_flagged = True
        elif not self.is_revealed:
            self.cell_btn_object.configure(bg="SystemButtonFace")
            self.is_flagged = False

    # Shows that the cell is a mine and alerts the user
    def show_mine(self):
        self.cell_btn_object.configure(bg="red")
        ctypes.windll.user32.MessageBoxW(0, "You set off a mine!", "Game Over", 0)
        sys.exit()

    # Shows the number of mines around the cell and updates cell count label
    def show_cell(self):
        if not self.is_revealed:
            Cell.cell_count -= 1
            self.is_revealed = True
            self.cell_btn_object.configure(text=f"{self.surrounding_mines}")
            Cell.cell_count_label_object.configure(text=f"{Cell.cell_count}")

            if self.surrounding_mines == 0:
                for single_cell in self.get_surrounding_cells():
                    single_cell.show_cell()

    # Get list of surrounding cells
    def get_surrounding_cells(self):
        surrounding_cells = [
            Cell.get_cell_by_position(self.x - 1, self.y - 1),
            Cell.get_cell_by_position(self.x, self.y - 1),
            Cell.get_cell_by_position(self.x + 1, self.y - 1),
            Cell.get_cell_by_position(self.x - 1, self.y),
            Cell.get_cell_by_position(self.x + 1, self.y),
            Cell.get_cell_by_position(self.x - 1, self.y + 1),
            Cell.get_cell_by_position(self.x, self.y + 1),
            Cell.get_cell_by_position(self.x + 1, self.y + 1)
        ]

        surrounding_cells = [single_cell for single_cell in surrounding_cells if single_cell is not None]
        return surrounding_cells

    # Increment surrounding mine number for each surrounding cell
    def increment_surrounding_cell_numbers(self):
        surrounding_cells = self.get_surrounding_cells()

        for single_cell in surrounding_cells:
            if single_cell is not None:
                single_cell.surrounding_mines += 1

    # Makes some cells contain mines and update surrounding cells
    @staticmethod
    def randomize_mines():
        selected_cells = random.sample(Cell.all_cells, settings.MINES_COUNT)
        for single_cell in selected_cells:
            single_cell.is_mine = True
            single_cell.increment_surrounding_cell_numbers()

    # Return cell based on x,y values, or None if cell doesn't exist
    @staticmethod
    def get_cell_by_position(x, y):
        if 0 <= x < settings.GRID_SIZE and 0 <= y < settings.GRID_SIZE:
            return Cell.all_cells[x + (settings.GRID_SIZE * y)]
        else:
            return None

    # Creates a label object for this cell
    @staticmethod
    def create_cell_count_label(location):
        Cell.cell_count_label_object = Label(
            location,
            width=12,
            height=2,
            bg="black",
            fg="white",
            font=("", 20),
            text=f"Cells Left:{Cell.cell_count}"
        )

    # Returned when Cell is called
    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
