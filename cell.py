from tkinter import *
import random
import settings
import ctypes
import sys


class Cell:
    all_cells = []
    cell_count = 0
    mine_count = 0
    size = 0
    cell_count_label_object = None
    first_move = False
    lost = False
    won = False

    image_default = None
    image_flag = None
    image_bomb = None
    image_numbers = []

    # Initializer
    def __init__(self, x, y, size, is_mine=False):
        self.is_mine = is_mine
        self.cell_btn_object = None
        self.x = x
        self.y = y
        self.surrounding_mines = 0
        self.is_revealed = False
        self.is_flagged = False

        Cell.size = size
        Cell.cell_count = size ** 2
        Cell.mine_count = (size ** 2) // 4
        Cell.all_cells.append(self)
        Cell.first_move = True

    # Creates a button object for this cell
    def create_btn_object(self, location):
        btn = Button(
            location,
            width=settings.WIDTH // Cell.size,
            height=settings.WIDTH // Cell.size,
            borderwidth=0,
            highlightthickness=0,
            image=Cell.image_default
        )
        btn.bind("<Button-1>", self.handle_left_click)
        btn.bind("<Button-3>", self.handle_right_click)
        self.cell_btn_object = btn

    # Action on left click, used to reveal cells
    def handle_left_click(self, event, ai=None):
        if Cell.first_move:
            Cell.randomize_mines(self)
            Cell.first_move = False
            self.show_cell(ai=ai)
        elif self.is_mine and not self.is_flagged:
            self.show_mine()
        elif not self.is_flagged:
            self.show_cell(ai=ai)
            if Cell.cell_count == Cell.mine_count:
                Cell.won = True
                Cell.show_all_cells()
                Cell.cell_count_label_object.configure(text="You Win!")

    # Action on right click, used to flag cells
    def handle_right_click(self, event):
        if not self.is_flagged and not self.is_revealed:
            self.cell_btn_object.configure(image=Cell.image_flag)
            self.is_flagged = True
        elif not self.is_revealed:
            self.cell_btn_object.configure(image=Cell.image_default)
            self.is_flagged = False

    # Shows that the cell is a mine and alerts the user
    def show_mine(self):
        if not self.is_revealed:
            self.cell_btn_object.configure(image=Cell.image_bomb)
            self.is_revealed = True
            Cell.lost = True
            Cell.show_all_cells()
            Cell.cell_count_label_object.configure(text="You Lose")

    # Shows the number of mines around the cell and updates cell count label
    def show_cell(self, ai=None):
        if not self.is_revealed:
            Cell.cell_count -= 1
            self.is_revealed = True
            self.cell_btn_object.configure(image=Cell.image_numbers[self.surrounding_mines])
            Cell.cell_count_label_object.configure(text="Cells Left: " + f"{Cell.cell_count - Cell.mine_count}")

            if (self.surrounding_mines == 0) and (ai is None):
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
        for single_cell in self.get_surrounding_cells():
            if single_cell is not None:
                single_cell.surrounding_mines += 1

    # Makes some cells contain mines and update surrounding cells
    @staticmethod
    def randomize_mines(cell):
        ignore_cells = cell.get_surrounding_cells()
        ignore_cells.append(cell)

        other_cells = [single_cell for single_cell in Cell.all_cells if single_cell not in ignore_cells]

        selected_cells = random.sample(other_cells, Cell.mine_count)
        for single_cell in selected_cells:
            single_cell.is_mine = True
            single_cell.increment_surrounding_cell_numbers()

    # Return cell based on x,y values, or None if cell doesn't exist
    @staticmethod
    def get_cell_by_position(x, y):
        if 0 <= x < Cell.size and 0 <= y < Cell.size:
            return Cell.all_cells[x + (Cell.size * y)]
        else:
            return None

    # Creates a label object for this cell
    @staticmethod
    def create_cell_count_label(location):
        Cell.cell_count_label_object = Label(
            location,
            width=12,
            height=2,
            bg="gray",
            fg="white",
            font=("", 20),
            text=f"Cells Left:{Cell.cell_count - Cell.mine_count}"
        )

    # Show all remaining cells
    @staticmethod
    def show_all_cells():
        for single_cell in Cell.all_cells:
            if not single_cell.is_revealed:
                if single_cell.is_mine:
                    single_cell.cell_btn_object.configure(image=Cell.image_bomb)
                    single_cell.is_revealed = True
                else:
                    single_cell.cell_btn_object.configure(image=Cell.image_numbers[single_cell.surrounding_mines])
                    single_cell.is_revealed = True

    # Returned when Cell is called
    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
