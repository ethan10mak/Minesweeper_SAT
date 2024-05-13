# File for solving the minesweeper problem
import sys

from pycryptosat import Solver
import numpy as np

rows = 3
columns = 3
dim = rows * columns
mine = 9
undiscovered = 10

# Maybe shouldn't include undiscovered (need to find how to set areas as mines)
k_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


class sat_solve:
    def __init__(self):
        self.rows = 3
        self.columns = 3
        self.dim = self.rows * self.columns
        self.mine = 9
        self.k_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Returns the corresponding variable number
    # Ex var(i, j, k) represents variable x at row i, column j, and value k

    def var(i, j, k):
        return (i - 1) * rows * columns + (j - 1) * columns + (k - 1) + 1

    # return

    # board: gives state of board
    # i: i as integer
    # j: j as integer
    def check_mines(board, i, j):
        state = board[i][j]
        tiles = []
        count = 0
        if state == mine:
            return []
        if state == undiscovered:
            return []

        for a in range(-1, 2):
            for b in range(-1, 2):
                if (a + i > 0 and a + 1 < rows - 1) and (
                    b + j > 0 and b + j < columns - 1
                ):
                    if board[i + a][j + b] == undiscovered:
                        tiles.append([i + a, j + b])
                        count += 1

        if count == state:
            return tiles
        return []

    def solve(self, board):
        # k_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        clauses = []
        for i in range(1, rows + 1):
            for j in range(1, columns + 1):
                # C1 the entry at row i col j has at least one value
                clauses.append([self.var(i, j, k) for k in k_values])

                # C2 the entry at row i col j has at most on value
                for k in range(1, len(k_values) + 1):
                    for l in range(k + 1, len(k_values) + 1):
                        clauses.append([-self.var(i, j, k), -self.var(i, j, l)])

        for i in range(0, rows):
            for j in range(0, columns):
                # If the state number equals the number of undiscovered squares next to it,
                # Create a clause that sets the undiscovered squares to mines
                mines = self.check_mines(board, i, j)
                if mines != []:
                    print(mines)
                    for m in mines:
                        clauses.append([self.var(m[0], m[1], 9)])

        s = Solver()
        for clause in clauses:
            print(clause)
            s.add_clause(clause)
        sat, solution = s.solve()
        print(sat)
        print(solution)
