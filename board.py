# The game board representing Minesweeper
# Responsible for outputting the current state of the board and setting up the game board.
# Installed pycryptosat
# Run line pip install pycryptosat
import numpy as np
import random

from sat_solver import sat_solve
from guess import guesser


rows = 16
columns = 30
total_mines = 99
dim = rows * columns
spaces = dim - total_mines

mine = 9
undiscovered = 10
safe = 11
flag = 12


def rev_var(n):
    i = 0
    j = 0
    k = 0
    div_i = 11 * 11
    div_j = 11
    if columns > 11:
        div_i = columns * columns
        div_j = columns
    if n > div_i:
        i = (n - 1) // div_i
        n = n - (i * div_i)
    if n > div_j:
        j = (n - 1) // (div_j)
        n = n - (j * div_j)
    k = n
    return [i, j, k]


def get_board_position(board, i, j):
    return board[i][j]


def print_board(board):
    for i in board:
        for j in i:
            if j == 9:
                print(" *", end="")
            elif j == 10:
                print(" X", end="")
            elif j == 12:
                print(" F", end="")
            else:
                print(" " + str(j), end="")
        print("")
    return 0


def get_mines(board):
    count = total_mines
    for i in range(0, rows):
        for j in range(0, columns):
            if board[i][j] == 12:
                count -= 1
    return count


# Generate Mine board function
def mine_board(r, c, n, first, setup):
    if setup == -1:
        random.seed()
        mines = []
        for x in range(0, n):
            check = True
            i = -1
            j = -1
            while check == True:
                check = False
                i = random.randint(0, r - 1)
                j = random.randint(0, c - 1)
                if [i, j] == first or [i, j] in mines:
                    check = True
                for a in range(-1, 2):
                    for b in range(-1, 2):
                        if (a + first[0] > -1 and a + first[0] < rows) and (
                            b + first[1] > -1 and b + first[1] < columns
                        ):
                            if first[0] + a == i and first[1] + b == j:
                                check = True
            mines.append([i, j])

        board = []
        for i in range(0, r):
            temp_list = []
            for j in range(0, c):
                if [i, j] in mines:
                    temp_list.append(9)
                else:
                    temp_list.append(10)
            board.append(temp_list)

        return board

    else:
        random.seed()
        mines = []
        x = 0
        while x < n:
            x += 1
            print(x)
            check = True
            i = -1
            j = -1
            step = 20
            while check == True:
                check = False
                i = random.randint(0, r - 1)
                j = random.randint(0, c - 1)
                if [i, j] == first or [i, j] in mines:
                    check = True
                for a in range(-1, 2):
                    for b in range(-1, 2):
                        if (a + first[0] > -1 and a + first[0] < rows) and (
                            b + first[1] > -1 and b + first[1] < columns
                        ):
                            if first[0] + a == i and first[1] + b == j:
                                check = True
                if check != True:

                    if x == n:

                        answer = []
                        for y in range(0, r):
                            temp_list = []
                            for z in range(0, c):
                                if [y, z] in mines or [y, z] == [i, j]:
                                    temp_list.append(9)
                                else:
                                    temp_list.append(10)
                            answer.append(temp_list)
                        answer = generate_numbers(answer, r, c)
                        # print_board(answer)
                        current_board = create_empty_board(rows, columns)
                        # print_board(current_board)
                        take_turn(answer, current_board, [first[0], first[1]], False)
                        # print_board(current_board)
                        changed = True
                        while changed == True:
                            changed = solve_current_state(
                                current_board, answer, get_mines(current_board)
                            )
                            state = game_state(current_board, answer)
                            print_board(current_board)
                            print("Mines Left: " + str(get_mines(current_board)))
                            if state == "Win":
                                print("OK")

                                break
                        if changed == False:
                            print_board(answer)
                            check = True
                            for mine in mines:
                                if current_board[mine[0]][mine[1]] == undiscovered:
                                    mines.remove(mine)
                                    x -= 1
            mines.append([i, j])

        board = []
        for i in range(0, r):
            temp_list = []
            for j in range(0, c):
                if [i, j] in mines:
                    temp_list.append(9)
                else:
                    temp_list.append(10)
            board.append(temp_list)
        print("Done generating")
        return board


def create_empty_board(r, c):
    board = []
    for i in range(0, r):
        temp_list = []
        for j in range(0, c):
            temp_list.append(10)
        board.append(temp_list)
    return board


# Generate Numbers in different board function
# Given mine board, give numbers that represent how many mines are next to it
# The result is the final solution of the board
def generate_numbers(board, r, c):
    new_board = board
    for i in range(0, r):
        for j in range(0, c):
            if new_board[i][j] != mine:
                count = 0
                for a in range(-1, 2):
                    for b in range(-1, 2):
                        if (a + i > -1 and a + i < rows) and (
                            b + j > -1 and b + j < columns
                        ):
                            if new_board[i + a][j + b] == mine:
                                count += 1
                new_board[i][j] = count
    return new_board


def clear_zeros(answer, current, i, j):
    if current[i][j] != 0:
        current[i][j] = answer[i][j]
        return current
    for a in range(-1, 2):
        for b in range(-1, 2):
            if (a + i > -1 and a + i < rows) and (b + j > -1 and b + j < columns):
                if not (a == 0 and b == 0):
                    if current[i + a][j + b] != answer[i + a][j + b]:
                        current[i + a][j + b] = answer[i + a][j + b]
                        current = clear_zeros(answer, current, i + a, j + b)
                    else:
                        current[i + a][j + b] = answer[i + a][j + b]
                    # current = clear_zeros(answer, current, i + a, j + b)

    return current


def get_spaces_to_win(board, answer):
    count = 0
    for i in range(0, rows):
        for j in range(0, columns):
            if board[i][j] == 10 and answer[i][j] != 9:
                count += 1
    return count


def get_mine_triggered(board):
    for i in range(0, rows):
        for j in range(0, columns):
            if board[i][j] == 9:
                return True
    return False


# Returns the current state of the game
def game_state(current, answer):
    count = 0
    for i in range(0, rows):
        for j in range(0, columns):
            if current[i][j] == 9:
                return "Lose"
            elif current[i][j] == 10 and answer[i][j] != 9:
                count += 1
    if count == 0:
        return "Win"
    return "Play"


# answer: the board answer with all revealed squares
# current: the current state of the board (what the player sees)
# tile: the tile as [row, column]
# flag: Boolean, True if flaggin for mine, False if checking square
# Returns current state of board after tile is flagged or searched
def take_turn(answer, current, tile, flag):
    if flag:
        current[tile[0]][tile[1]] = 12
    else:
        current[tile[0]][tile[1]] = answer[tile[0]][tile[1]]
        clear_zeros(answer, current, tile[0], tile[1])
        if current[tile[0]][tile[1]] == mine:
            mine_triggered = True
            # print_board(current)
            # print_board(answer)
            # print("Mines Left: " + str(get_mines(current)))
            # print("GAME OVER!!!")
            return current
            # exit(0)
        if get_spaces_to_win(current, answer) == 0:
            # print_board(current)
            # print("Mines Left: " + str(get_mines(current)))
            # print("You win!!")
            return current
            # exit(0)

    return current


# solve_current_state
def solve_current_state(current_board, board_answer, mines):
    prev_board = []
    for i in current_board:
        temp = []
        for j in i:
            temp.append(j)
        prev_board.append(temp)
    [sat, solution] = sat_solve.solve(sat_solve, current_board, mines)
    for i in range(1, len(solution)):
        [a, b, c] = rev_var(i)
        base = 11
        if columns > 11:
            base = columns
        decider = 0
        if base > 11:
            decider = 11
        if i % base == decider and solution[i] == True:
            current_board = take_turn(board_answer, current_board, [a, b], False)
            clear_zeros(board_answer, current_board, a, b)
        if i % base == 9 and solution[i] == True:
            current_board = take_turn(board_answer, current_board, [a, b], True)
        state = game_state(current_board, board_answer)
        if state == "Win" or state == "Lose":
            return True
    # changed = False
    for i in range(0, rows):
        for j in range(0, columns):
            if prev_board[i][j] != current_board[i][j]:
                return True
    return False


class board:
    def __init__(self):
        self.rows = 11
        self.columns = 11
        self.dim = self.rows * self.columns
        self.mine = 9
        self.k_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    def play(r, c, fast, setup):
        # States: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
        # 0 = No mines next to it
        # 9 = mine
        # 10 = Not Discovered

        current_board = create_empty_board(rows, columns)
        print_board(current_board)
        # r = int(input("What is your row?"))
        # c = int(input("What is your column?"))

        board_answer = mine_board(rows, columns, total_mines, [r, c], setup)
        board_answer = generate_numbers(board_answer, rows, columns)
        current_board = take_turn(board_answer, current_board, [r, c], False)
        # while True:
        #    r = int(input("What is your row?"))
        #    c = int(input("What is your column?"))
        #    current_board = take_turn(board_answer, current_board, [r, c], False)
        #    print_board(current_board)
        while True:
            if fast == False:
                input("Next Move")
            changed = solve_current_state(
                current_board, board_answer, get_mines(current_board)
            )
            print_board(current_board)
            print("Mines Left: " + str(get_mines(current_board)))
            state = game_state(current_board, board_answer)
            if state == "Win":
                print_board(board_answer)
                print("Mines Left: " + str(get_mines(current_board)))
                print("You win!!")
                return "Win"
            elif state == "Lose":
                print_board(current_board)
                print_board(board_answer)
                print("Mines Left: " + str(get_mines(current_board)))
                print("GAME OVER!!!")
                return "Lose"
            # If the SAT solver stagnates
            if changed == False:
                comb = guesser.guess_safe(
                    guesser, current_board, get_mines(current_board)
                )
                print("Unchanged")
                take_turn(board_answer, current_board, comb, False)
                state = game_state(current_board, board_answer)
                if state == "Win":
                    print_board(board_answer)
                    print("Mines Left: " + str(get_mines(current_board)))
                    print("You win!!")
                    return "Win"
                elif state == "Lose":
                    print_board(current_board)
                    print_board(board_answer)
                    print("Mines Left: " + str(get_mines(current_board)))
                    print("GAME OVER!!!")
                    return "Lose"
                print_board(current_board)
                print("Mines Left: " + str(get_mines(current_board)))
                """
                changed = solve_current_state(
                    current_board, board_answer, get_mines(current_board)
                )
                state = game_state(current_board, board_answer)
                if state == "Win":
                    return "Win"
                elif state == "Lose":
                    return "Lose"
                """
