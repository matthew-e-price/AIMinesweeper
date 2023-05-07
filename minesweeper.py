import random


# n = grid size, b = number of bombs
def make_game_board(n, b):
    board_array = [[0 for row in range(n)] for column in range(n)]

    for num in range(b):
        loop = True
        while loop:
            y = random.randint(0, n - 1)
            x = random.randint(0, n - 1)
            if board_array[y][x] != "X":
                board_array[y][x] = "X"
                loop = False

        if 1 <= x <= n - 2:
            # Adds to the left and right
            if board_array[y][x + 1] != "X":
                board_array[y][x + 1] += 1
            if board_array[y][x - 1] != "X":
                board_array[y][x - 1] += 1
        if x == 0:
            # Adds to the right
            if board_array[y][x + 1] != "X":
                board_array[y][x + 1] += 1
        if x == n - 1:
            # Adds to the left
            if board_array[y][x - 1] != "X":
                board_array[y][x - 1] += 1

        if (1 <= x <= n - 1) and (1 <= y <= n - 1):
            # Adds to the top left
            if board_array[y - 1][x - 1] != "X":
                board_array[y - 1][x - 1] += 1
        if (0 <= x <= n - 2) and (1 <= y <= n - 1):
            # Adds to the top right
            if board_array[y - 1][x + 1] != "X":
                board_array[y - 1][x + 1] += 1
        if (0 <= x <= n - 1) and (1 <= y <= n - 1):
            # Adds to the top center
            if board_array[y - 1][x] != "X":
                board_array[y - 1][x] += 1

        if (0 <= x <= n - 2) and (0 <= y <= n - 2):
            # Adds to the bottom right
            if board_array[y + 1][x + 1] != "X":
                board_array[y + 1][x + 1] += 1
        if (1 <= x <= n - 1) and (0 <= y <= n - 2):
            # Adds to the bottom left
            if board_array[y + 1][x - 1] != "X":
                board_array[y + 1][x - 1] += 1
        if (0 <= x <= n - 1) and (0 <= y <= n - 2):
            # Adds to the bottom center
            if board_array[y + 1][x] != "X":
                board_array[y + 1][x] += 1

    return board_array


def make_player_board(n):
    player_array = [["-" for row in range(n)] for column in range(n)]
    return player_array


def display_board(board):
    for row in board:
        print(" ".join(str(cell) for cell in row))
        print("")


def check_for_win(player_array):
    for row in player_array:
        for cell in row:
            if cell == "-":
                return False
    return True


def continue_game(score):
    print("Score: ", score)
    is_continue = input("Do you want to try again? (Y/N) :")
    if is_continue.lower() == "n":
        return False
    return True


def minesweeper():
    keep_playing = True
    while keep_playing:
        difficulty = input("Select your difficulty\nBeginner: 1\nIntermediate: 2\nHard: 3\n")
        if difficulty == '1':
            n = 5
            k = 3
        elif difficulty == '2':
            n = 6
            k = 8
        else:
            n = 8
            k = 20

        minesweeper_board = make_game_board(n, k)
        player_board = make_player_board(n)
        score = 0

        while True:
            if not check_for_win(player_board):
                print("Enter your cell you want to open: ")
                x = input("X (1 to " + str(n) + "): ")
                y = input("Y (1 to " + str(n) + "): ")
                x = int(x) - 1
                y = int(y) - 1

                if minesweeper_board[y][x] == 'X':
                    print("Game Over!")
                    display_board(minesweeper_board)
                    keep_playing = continue_game(score)
                    break
                else:
                    player_board[y][x] = minesweeper_board[y][x]
                    display_board(player_board)
                    score += 1

            else:
                display_board(player_board)
                print("You have Won!")
                keep_playing = continue_game(score)
                break


if __name__ == "__main__":
    try:
        minesweeper()
    except KeyboardInterrupt:
        print('\nEnd of Game. Bye Bye!')
