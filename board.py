# The game board representing Minesweeper
# Responsible for outputting the current state of the board and setting up the game board.
# Installed pycryptosat
# Run line pip install pycryptosat
import numpy as np
from sat_solver import sat_solve
import random

rows = 3
columns = 3
dim = rows * columns


def get_board_position(board, i, j):
    return board[i][j]


def print_board(board):
    for i in board:
        for j in i:
            if j == 9:
                print(" *", end="")
            elif j == 10:
                print(" X", j, end="")
            else:
                print(" " + str(j), end="")
        print("")
    return 0


# Generate Mine board function
def mine_board(r, c, n, first):
    random.seed()
    mines = []
    for x in range(0, n):
        i = random.randint(0, r - 1)
        j = random.randint(0, c - 1)
        while [i, j] == first or [i, j] in mines:
            i = random.randint(0, r - 1)
            j = random.randint(0, c - 1)
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


# Generate Numbers in different board function
# Given mine board, give numbers that represent how many mines are next to it
# The result is the final solution of the board
def generate_numbers(board, r, c):
    for i in range(0, r):
        for j in range(0, c):
            if board[i][j] != mine:
                count = 0
                for a in range(-1, 2):
                    for b in range(-1, 2):
                        if (a + i > -1 and a + i < rows) and (
                            b + j > -1 and b + j < columns
                        ):
                            if board[i + a][j + b] == mine:
                                count += 1
                board[i][j] = count
    return board


# solve_current_state
def solve_current_state(current_board):
    sat_solve.solve(sat_solve, current_board)
    return 0


# States: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
# 0 = No mines next to it
# 9 = mine
# 10 = Not Discovered

mine = 9
undiscovered = 10
safe = 11
board = [[mine, 1, 0], [1, 1, 0], [0, 0, 0]]
board = mine_board(3, 3, 2, [1, 1])
board = generate_numbers(board, rows, columns)

print_board(board)
current_board = [
    [mine, undiscovered, undiscovered],
    [undiscovered, 1, undiscovered],
    [undiscovered, undiscovered, undiscovered],
]
# numbers_board = generate_numbers(mine_board)
solve_current_state(current_board)
