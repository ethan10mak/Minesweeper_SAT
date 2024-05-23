# File for solving the minesweeper problem
import sys

from pycryptosat import Solver
import numpy as np

rows = 10
columns = 10
dim = rows * columns
mine = 9
undiscovered = 10
safe = 11

k_values = [1, 2, 3, 4, 5, 6, 7, 8, mine, undiscovered, safe]


class sat_solve:
    def __init__(self):
        self.rows = 10
        self.columns = 10
        self.dim = self.rows * self.columns
        self.mine = 9
        self.k_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    # Returns the corresponding variable number
    # Ex var(i, j, k) represents variable x at row i, column j, and value k
    # original only worked with grid of 11 * 11 dimensions.
    # Need to find a formula that can return any dimensions
    def var(i, j, k):
        return (i * 16 * 30) + (j * 16) + k
        # return (i - 1) * rows * columns + (j - 1) * columns + (k - 1) + 1

    # board: gives state of board
    # i: i as integer
    # j: j as integer
    def check_mines(board, i, j):
        state = board[i][j]
        tiles = []
        count = 0
        if state == mine or state == 12:
            return []
        if state == undiscovered:
            return []
        for a in range(-1, 2):
            for b in range(-1, 2):
                if (a + i > -1 and a + i < rows) and (b + j > -1 and b + j < columns):
                    if board[i + a][j + b] == undiscovered:
                        tiles.append([i + a, j + b])
                        count += 1
                    if board[i + a][j + b] == mine or board[i + a][j + b] == 12:
                        state = state - 1
        if count == state:
            return tiles
        return []

    def check_safe(board, i, j):
        state = board[i][j]
        tiles = []
        count = 0
        if state == mine or state == undiscovered or state == 12:
            return []
        for a in range(-1, 2):
            for b in range(-1, 2):
                if (a + i > -1 and a + i < rows) and (b + j > -1 and b + j < columns):
                    if board[i + a][j + b] == mine or board[i + a][j + b] == 12:
                        count += 1
                    if board[i + a][j + b] == undiscovered:
                        tiles.append([i + a, j + b])
        if count == state:
            return tiles
        return []

    def solve(self, board):
        # k_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        clauses = []
        for i in range(0, rows):
            for j in range(0, columns):
                # C1 the entry at row i col j has at least one value
                clauses.append([self.var(i, j, k) for k in k_values])

                # C2 the entry at row i col j has at most on value
                for k in range(1, len(k_values)):
                    for l in range(k + 1, len(k_values)):
                        clauses.append([-self.var(i, j, k), -self.var(i, j, l)])

        for i in range(0, rows):
            for j in range(0, columns):
                # If the state number equals the number of undiscovered squares next to it,
                # Create a clause that sets the undiscovered squares to mines
                if board[i][j] in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    clauses.append([self.var(i, j, board[i][j])])

                mines = self.check_mines(board, i, j)
                if mines != []:
                    for m in mines:
                        clauses.append([self.var(m[0], m[1], 9)])

                safe = self.check_safe(board, i, j)

                if safe != []:
                    for s in safe:
                        clauses.append([self.var(s[0], s[1], 11)])

        s = Solver()
        for clause in clauses:
            print(clause)
            s.add_clause(clause)
        sat, solution = s.solve()
        # print(sat)
        # print(solution)
        return [sat, solution]
