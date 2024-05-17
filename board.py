# The game board representing Minesweeper
# Responsible for outputting the current state of the board and setting up the game board.
# Installed pycryptosat
# Run line pip install pycryptosat
import numpy as np
from sat_solver import sat_solve
import random

rows = 5
columns = 5
total_mines = 5
dim = rows * columns


def rev_var(n):
    i = 0
    j = 0
    k = 0
    if n > 121:
        i = (n - 1) // 121
        n = n - (i * 121)
        print(n)
    if n > 11:
        j = (n - 1) // 11
        n = n - (j * 11)
        print(n)
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
    print(mines)

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


def clear_zeros():
    return 0


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
    return current


# solve_current_state
def solve_current_state(current_board, board_answer):
    [sat, solution] = sat_solve.solve(sat_solve, current_board)
    for i in range(1, len(solution)):
        if i % 11 == 0 and solution[i] == True:
            [a, b, c] = rev_var(i)
            print("safe")
            print(rev_var(i))
            current_board = take_turn(board_answer, current_board, [a, b], False)
        if i % 9 == 0 and solution[i] == True:
            [a, b, c] = rev_var(i)
            print("flag")
            print(rev_var(i))
            current_board = take_turn(board_answer, current_board, [a, b], True)
    print_board(current_board)
    return 0


# States: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
# 0 = No mines next to it
# 9 = mine
# 10 = Not Discovered

mine = 9
undiscovered = 10
safe = 11
flag = 12
board_answer = mine_board(rows, columns, 5, [1, 1])
board_answer = generate_numbers(board_answer, rows, columns)
print_board(board_answer)
current_board = create_empty_board(rows, columns)
print_board(current_board)
current_board = take_turn(board_answer, current_board, [1, 1], False)
print_board(current_board)
# while True:
#    r = int(input("What is your row?"))
#    c = int(input("What is your column?"))
#    current_board = take_turn(board_answer, current_board, [r, c], False)
#    print_board(current_board)
while True:
    input("Next Move")
    solve_current_state(current_board, board_answer)
