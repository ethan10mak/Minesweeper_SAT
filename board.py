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


def get_spaces_to_win(board, answer):
    count = 0
    for i in range(0, rows):
        for j in range(0, columns):
            if board[i][j] == 10 and answer[i][j] != 9:
                count += 1
    return count


def get_mines(board):
    count = total_mines
    for i in range(0, rows):
        for j in range(0, columns):
            if board[i][j] == 12:
                count -= 1
    return count


# Generate Mine board function
def mine_board(r, c, n, first):
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
        clear_zeros(board_answer, current_board, tile[0], tile[1])
        if current[tile[0]][tile[1]] == mine:
            print_board(current)
            print("GAME OVER!!!")
            exit(0)
    return current_board


# solve_current_state
def solve_current_state(current_board, board_answer):
    prev_board = []
    for i in current_board:
        temp = []
        for j in i:
            temp.append(j)
        prev_board.append(temp)
    [sat, solution] = sat_solve.solve(sat_solve, current_board)
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
    print_board(current_board)
    # changed = False
    for i in range(0, rows):
        for j in range(0, columns):
            if prev_board[i][j] != current_board[i][j]:
                return True
    print("YES")
    return False


# States: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
# 0 = No mines next to it
# 9 = mine
# 10 = Not Discovered

mine = 9
undiscovered = 10
safe = 11
flag = 12


current_board = create_empty_board(rows, columns)
print_board(current_board)
r = int(input("What is your row?"))
c = int(input("What is your column?"))

board_answer = mine_board(rows, columns, total_mines, [r, c])
board_answer = generate_numbers(board_answer, rows, columns)
current_board = take_turn(board_answer, current_board, [r, c], False)

print_board(board_answer)
print()
print_board(current_board)
print("Mines Left: " + str(total_mines))
# while True:
#    r = int(input("What is your row?"))
#    c = int(input("What is your column?"))
#    current_board = take_turn(board_answer, current_board, [r, c], False)
#    print_board(current_board)
while True:
    input("Next Move")
    changed = solve_current_state(current_board, board_answer)
    print("Mines Left: " + str(get_mines(current_board)))
    if changed == False:
        comb = guesser.guess_safe(current_board, get_mines(current_board))
        print("Changed")
        for i in list(comb):
            print(i)
        exit(0)
