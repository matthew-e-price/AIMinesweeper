from tkinter import *
from cell import Cell
from PIL import Image, ImageTk
from ai import AI
import settings


# Create minesweeper board
def create_board_ui(size, location):
    for y in range(size):
        for x in range(size):
            c = Cell(x, y, size)
            c.create_btn_object(location)
            c.cell_btn_object.grid(column=x, row=y)


# Hide all frames and delete their children
def hide_frames():
    for element in menu_frame.winfo_children():
        element.destroy()
    for element in difficulty_frame.winfo_children():
        element.destroy()
    for element in ai_frame.winfo_children():
        element.destroy()
    for element in minesweeper_frame.winfo_children():
        element.destroy()

    menu_frame.pack_forget()
    difficulty_frame.pack_forget()
    ai_frame.pack_forget()
    minesweeper_frame.pack_forget()

    Cell.all_cells = []
    Cell.image_numbers = []
    Cell.lost = False
    Cell.won = False
    Cell.first_move = True


# Have the AI make the next step
def ai_step(ai, ai_step_btn):
    ai_move = ai.make_safe_move()
    if ai_move is None:
        ai.make_random_move()
    if Cell.lost:
        ai_step_btn.config(state="disabled")
    if Cell.won:
        ai_step_btn.config(state="disabled")


# Show menu frame
def show_menu_frame():
    menu_top_frame = Frame(menu_frame, bg="gray", width=settings.WIDTH, height=200)
    menu_bottom_frame = Frame(menu_frame, width=settings.WIDTH, height=500)

    menu_play_btn = Button(
        menu_bottom_frame,
        width=10,
        height=1,
        bg="#36A4FF",
        fg="white",
        font=("", 30),
        command=lambda: goto_difficulty_frame(),
        text="Play"
    )
    menu_ai_btn = Button(
        menu_bottom_frame,
        width=10,
        height=1,
        bg="#36A4FF",
        fg="white",
        font=("", 30),
        command=lambda: goto_ai_frame(),
        text="Test AI"
    )
    menu_title_lbl = Label(
        menu_top_frame,
        bg="gray",
        fg="white",
        font=("", 50),
        text="Minesweeper"
    )

    menu_top_frame.grid_propagate(False)
    menu_top_frame.grid_columnconfigure(0, weight=1)
    menu_top_frame.grid_rowconfigure(0, weight=1)
    menu_bottom_frame.grid_propagate(False)
    menu_bottom_frame.grid_columnconfigure(0, weight=1)
    menu_bottom_frame.grid_rowconfigure(0, weight=1)
    menu_bottom_frame.grid_rowconfigure(1, weight=1)

    menu_frame.pack()
    menu_top_frame.pack()
    menu_bottom_frame.pack(pady=100)

    menu_title_lbl.grid(column=0, row=0)
    menu_play_btn.grid(column=0, row=0)
    menu_ai_btn.grid(column=0, row=1)


# Show difficulty frame
def show_difficulty_frame():
    difficulty_top_frame = Frame(difficulty_frame, bg="gray", width=settings.WIDTH, height=200)
    difficulty_bottom_frame = Frame(difficulty_frame, width=settings.WIDTH, height=500)

    difficulty_easy = Button(
        difficulty_bottom_frame,
        width=10,
        height=1,
        bg="#36A4FF",
        fg="white",
        font=("", 30),
        command=lambda: goto_minesweeper_frame(10),
        text="Easy"
    )
    difficulty_medium = Button(
        difficulty_bottom_frame,
        width=10,
        height=1,
        bg="#36A4FF",
        fg="white",
        font=("", 30),
        command=lambda: goto_minesweeper_frame(15),
        text="Medium"
    )
    difficulty_hard = Button(
        difficulty_bottom_frame,
        width=10,
        height=1,
        bg="#36A4FF",
        fg="white",
        font=("", 30),
        command=lambda: goto_minesweeper_frame(20),
        text="Hard"
    )
    difficulty_title_lbl = Label(
        difficulty_top_frame,
        bg="gray",
        fg="white",
        font=("", 50),
        text="Minesweeper"
    )

    difficulty_top_frame.grid_propagate(False)
    difficulty_top_frame.grid_columnconfigure(0, weight=1)
    difficulty_top_frame.grid_rowconfigure(0, weight=1)
    difficulty_bottom_frame.grid_propagate(False)
    difficulty_bottom_frame.grid_columnconfigure(0, weight=1)
    difficulty_bottom_frame.grid_rowconfigure(0, weight=1)
    difficulty_bottom_frame.grid_rowconfigure(1, weight=1)
    difficulty_bottom_frame.grid_rowconfigure(2, weight=1)

    difficulty_frame.pack()
    difficulty_top_frame.pack()
    difficulty_bottom_frame.pack(pady=100)

    difficulty_title_lbl.grid(column=0, row=0)
    difficulty_easy.grid(column=0, row=0)
    difficulty_medium.grid(column=0, row=1)
    difficulty_hard.grid(column=0, row=2)


# Show AI frame
def show_ai_frame():
    n = settings.WIDTH // 10
    Cell.image_default = ImageTk.PhotoImage((Image.open(settings.IMG_DEFAULT)).resize((n, n)))
    Cell.image_flag = ImageTk.PhotoImage((Image.open(settings.IMG_FLAG)).resize((n, n)))
    Cell.image_bomb = ImageTk.PhotoImage((Image.open(settings.IMG_BOMB)).resize((n, n)))
    Cell.image_numbers.append(ImageTk.PhotoImage((Image.open(settings.IMG_ZERO)).resize((n, n))))
    Cell.image_numbers.append(ImageTk.PhotoImage((Image.open(settings.IMG_ONE)).resize((n, n))))
    Cell.image_numbers.append(ImageTk.PhotoImage((Image.open(settings.IMG_TWO)).resize((n, n))))
    Cell.image_numbers.append(ImageTk.PhotoImage((Image.open(settings.IMG_THREE)).resize((n, n))))
    Cell.image_numbers.append(ImageTk.PhotoImage((Image.open(settings.IMG_FOUR)).resize((n, n))))
    Cell.image_numbers.append(ImageTk.PhotoImage((Image.open(settings.IMG_FIVE)).resize((n, n))))
    Cell.image_numbers.append(ImageTk.PhotoImage((Image.open(settings.IMG_SIX)).resize((n, n))))
    Cell.image_numbers.append(ImageTk.PhotoImage((Image.open(settings.IMG_SEVEN)).resize((n, n))))
    Cell.image_numbers.append(ImageTk.PhotoImage((Image.open(settings.IMG_EIGHT)).resize((n, n))))

    minesweeper_top_frame = Frame(minesweeper_frame, bg="gray", width=settings.WIDTH, height=100)
    minesweeper_bottom_frame = Frame(minesweeper_frame, width=settings.WIDTH, height=800)

    minesweeper_top_frame.grid_propagate(False)
    minesweeper_top_frame.grid_columnconfigure(0, weight=1)
    minesweeper_top_frame.grid_columnconfigure(1, weight=1)
    minesweeper_top_frame.grid_columnconfigure(2, weight=1)
    minesweeper_top_frame.grid_rowconfigure(0, weight=1)
    minesweeper_bottom_frame.grid_propagate(False)

    minesweeper_frame.pack()
    minesweeper_top_frame.pack()
    minesweeper_bottom_frame.pack()

    create_board_ui(size=10, location=minesweeper_bottom_frame)

    Cell.create_cell_count_label(minesweeper_top_frame)
    ai_step_btn = Button(
        minesweeper_top_frame,
        width=12,
        height=1,
        bg="#36A4FF",
        fg="white",
        font=("", 20),
        command=lambda: ai_step(agent, ai_step_btn),
        text="Take next step"
    )
    ai_quit_btn = Button(
        minesweeper_top_frame,
        width=12,
        height=1,
        bg="#36A4FF",
        fg="white",
        font=("", 20),
        command=lambda: goto_menu_frame(),
        text="Return to menu"
    )

    Cell.cell_count_label_object.grid(column=0, row=0)
    ai_step_btn.grid(column=1, row=0)
    ai_quit_btn.grid(column=2, row=0)

    agent = AI(10)

    for selected_cell in Cell.all_cells:
        selected_cell.cell_btn_object.unbind("<Button-1>")
        selected_cell.cell_btn_object.unbind("<Button-3>")


# Show minesweeper frame
def show_minesweeper_frame(size):
    n = settings.WIDTH // size
    Cell.image_default = ImageTk.PhotoImage((Image.open(settings.IMG_DEFAULT)).resize((n, n)))
    Cell.image_flag = ImageTk.PhotoImage((Image.open(settings.IMG_FLAG)).resize((n, n)))
    Cell.image_bomb = ImageTk.PhotoImage((Image.open(settings.IMG_BOMB)).resize((n, n)))
    Cell.image_numbers.append(ImageTk.PhotoImage((Image.open(settings.IMG_ZERO)).resize((n, n))))
    Cell.image_numbers.append(ImageTk.PhotoImage((Image.open(settings.IMG_ONE)).resize((n, n))))
    Cell.image_numbers.append(ImageTk.PhotoImage((Image.open(settings.IMG_TWO)).resize((n, n))))
    Cell.image_numbers.append(ImageTk.PhotoImage((Image.open(settings.IMG_THREE)).resize((n, n))))
    Cell.image_numbers.append(ImageTk.PhotoImage((Image.open(settings.IMG_FOUR)).resize((n, n))))
    Cell.image_numbers.append(ImageTk.PhotoImage((Image.open(settings.IMG_FIVE)).resize((n, n))))
    Cell.image_numbers.append(ImageTk.PhotoImage((Image.open(settings.IMG_SIX)).resize((n, n))))
    Cell.image_numbers.append(ImageTk.PhotoImage((Image.open(settings.IMG_SEVEN)).resize((n, n))))
    Cell.image_numbers.append(ImageTk.PhotoImage((Image.open(settings.IMG_EIGHT)).resize((n, n))))

    minesweeper_top_frame = Frame(minesweeper_frame, bg="gray", width=settings.WIDTH, height=100)
    minesweeper_bottom_frame = Frame(minesweeper_frame, width=settings.WIDTH, height=800)

    minesweeper_top_frame.grid_propagate(False)
    minesweeper_top_frame.grid_columnconfigure(0, weight=1)
    minesweeper_top_frame.grid_columnconfigure(1, weight=1)
    minesweeper_top_frame.grid_rowconfigure(0, weight=1)
    minesweeper_bottom_frame.grid_propagate(False)

    minesweeper_frame.pack()
    minesweeper_top_frame.pack()
    minesweeper_bottom_frame.pack()

    create_board_ui(size=size, location=minesweeper_bottom_frame)

    Cell.create_cell_count_label(minesweeper_top_frame)
    minesweeper_quit_btn = Button(
        minesweeper_top_frame,
        width=12,
        height=1,
        bg="#36A4FF",
        fg="white",
        font=("", 20),
        command=lambda: goto_menu_frame(),
        text="Return to home"
    )

    Cell.cell_count_label_object.grid(column=0, row=0)
    minesweeper_quit_btn.grid(column=1, row=0)


# Change to the menu frame
def goto_menu_frame():
    hide_frames()
    show_menu_frame()


# Change to the difficulty frame
def goto_difficulty_frame():
    hide_frames()
    show_difficulty_frame()


# Change to the difficulty frame
def goto_minesweeper_frame(size):
    hide_frames()
    show_minesweeper_frame(size)


# Change to the difficulty frame
def goto_ai_frame():
    hide_frames()
    show_ai_frame()


# Creates a gui instance
root = Tk()

# Sets configurations for the window
root.geometry(str(settings.WIDTH) + "x" + str(settings.HEIGHT))
root.title("Minesweeper")
root.resizable(False, False)

# Menu frame
menu_frame = Frame(root, width=settings.WIDTH, height=settings.HEIGHT)

# Difficulty frame
difficulty_frame = Frame(root, width=settings.WIDTH, height=settings.HEIGHT)

# AI options frame
ai_frame = Frame(root, width=settings.WIDTH, height=settings.HEIGHT)

# Minesweeper game frame
minesweeper_frame = Frame(root, width=settings.WIDTH, height=settings.HEIGHT)

# Create the default frame
show_menu_frame()

# Run a window that won't close until X at top right is used
root.mainloop()
