# The game board representing Minesweeper
# Responsible for outputting the current state of the board and setting up the game board.
# Installed pycryptosat
# Run line pip install pycryptosat
import numpy as np
from sat_solver import sat_solve

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
            else:
                print("", j, end="")
        print("")
    return 0


# Generate Mine board function
def mine_board():
    return [[9, 10, 10], [10, 10, 10], [10, 10, 9]]


# Generate Numbers in different board function
# Given mine board, give numbers that represent how many mines are next to it
# The result is the final solution of the board
def generate_numbers(board):
    return [[mine, 1, 0], [1, 2, 1], [0, 1, mine]]


# solve_current_state
def solve_current_state(current_board, numbers_board):
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
# current_board = [[undiscovered, 1, 0], [1, 1, 0], [0, 0, 0]]
current_board = [
    [mine, undiscovered, undiscovered],
    [undiscovered, 1, undiscovered],
    [undiscovered, undiscovered, undiscovered],
]
# current_board = [[10, 10, 10], [10, 10, 10], [0, 10, 10]]
numbers_board = generate_numbers(mine_board)
solve_current_state(current_board, numbers_board)
