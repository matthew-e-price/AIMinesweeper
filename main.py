from tkinter import *
from cell import Cell
import settings


# Creates a gui instance
root = Tk()

# Sets configurations for the window
root.geometry(str(settings.WIDTH) + "x" + str(settings.HEIGHT))
root.title("Minesweeper")
root.resizable(False, False)
root.configure(bg="#a3a3a2")

# Set layout of the UI
top_frame = Frame(
    root,
    bg="#70706f",
    width=settings.WIDTH,
    height=120
)
top_frame.place(x=0, y=0)

middle_frame = Frame(
    root,
    bg="#70706f",
    width=settings.WIDTH,
    height=80
)
middle_frame.place(x=0, y=120)

bottom_frame = Frame(
    root,
    bg="#a3a3a2",
    width=settings.WIDTH,
    height=520
)
bottom_frame.place(x=0, y=200)

# Create title for the game
game_title = Label(
    top_frame,
    bg="#70706f",
    text="Minesweeper",
    font=("", 48)
)
game_title.place(relx=0.5, rely=0.5, anchor=CENTER)

# Create cells for the game board
for y in range(settings.GRID_SIZE):
    for x in range(settings.GRID_SIZE):
        c = Cell(x, y)
        c.create_btn_object(bottom_frame)
        c.cell_btn_object.grid(column=x, row=y)

# Create a label to track remaining cells to discover
Cell.create_cell_count_label(middle_frame)
Cell.cell_count_label_object.place(x=0, y=0)

# Randomize the mine locations
Cell.randomize_mines()

# Run a window that won't close until X at top right is used
root.mainloop()
