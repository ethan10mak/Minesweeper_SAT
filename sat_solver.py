# File for solving the minesweeper problem
import sys

from pycryptosat import Solver
import numpy as np

rows = 3
columns = 3
dim = rows * columns
mine = 9
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

    def check_squares_around(board, i, j):
        return

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

        # for i in range(1, rows + 1):
        #    for j in range(1, columns + 1):
        # Blan

        s = Solver()
        for clause in clauses:
            print(clause)
            s.add_clause(clause)
        sat, solution = s.solve()
        print(sat)
        print(solution)
