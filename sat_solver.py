# File for solving the minesweeper problem
import sys

from pycryptosat import Solver
import numpy as np

rows = 16
columns = 30
dim = rows * columns
mine = 9
undiscovered = 10
safe = 11
flag = 12
chance = 13

k_values = [1, 2, 3, 4, 5, 6, 7, 8, mine, undiscovered, safe]


class sat_solve:
    def __init__(self):
        self.rows = 11
        self.columns = 11
        self.dim = self.rows * self.columns
        self.mine = 9
        self.k_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    # Returns the corresponding variable number
    # Ex var(i, j, k) represents variable x at row i, column j, and value k
    # original only worked with grid of 11 * 11 dimensions.
    # Need to find a formula that can return any dimensions
    def var(i, j, k):
        if columns < 11:
            return (i * 11 * 11) + (j * 11) + k
        else:
            return (i * columns * columns) + (j * columns) + k
        # return (i - 1) * rows * columns + (j - 1) * columns + (k - 1) + 1

    # Checks surrounding area of tile if undiscovered area are mines
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

    # Checks surrounding area of tile if undiscovered area is safe
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

    # Follows 1-1-x pattern
    # Deals with 50/50 problem
    def advanced_check_safe(board, i, j):
        state = board[i][j]
        un_tiles = []
        num_tiles = []
        count = 0
        mine_count = 0
        if state == mine or state == undiscovered or state == 12:
            return []
        for a in range(-1, 2):
            for b in range(-1, 2):
                if (a + i > -1 and a + i < rows) and (b + j > -1 and b + j < columns):
                    if board[i + a][j + b] == mine or board[i + a][j + b] == 12:
                        mine_count += 1
                    if board[i + a][j + b] == undiscovered:
                        un_tiles.append([i + a, j + b])
                        count += 1
                    else:
                        num_tiles.append([i + a, j + b])
        if count != 2 and mine_count == (state - 1):
            return []

        for [x, y] in num_tiles:
            safe_tiles = []
            # print([x, y])
            mine_count = 0
            unshared_count = 0
            for a in range(-1, 2):
                for b in range(-1, 2):
                    if (a + x > -1 and a + x < rows) and (
                        b + y > -1 and b + y < columns
                    ):
                        if (
                            board[x + a][y + b] == undiscovered
                            and ([x, y] in un_tiles) == False
                        ):
                            safe_tiles.append([x + a, y + b])
                            unshared_count += 1
                        # elif (
                        #    board[x + a][y + b] == undiscovered
                        #    and ([x, y] in un_tiles) == True
                        # ):
                        #    shared_count += 1
                        elif board[x + a][y + b] == mine or board[x + a][y + b] == 12:
                            mine_count -= 1
            if unshared_count == board[x][y] and board[x][y] == (mine_count - 1):
                print("Found Safe")
                print(count)
                print(mine_count)
                print([x, y])
                print(safe_tiles)
                return safe_tiles
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
                if board[i][j] in [1, 2, 3, 4, 5, 6, 7, 8]:
                    clauses.append([self.var(i, j, board[i][j])])
                # Checks surrounding area for mines
                mines = self.check_mines(board, i, j)
                if mines != []:
                    for m in mines:
                        clauses.append([self.var(m[0], m[1], 9)])
                # Checks surrounding area for safe area
                safe = self.check_safe(board, i, j)
                if safe != []:
                    for s in safe:
                        clauses.append([self.var(s[0], s[1], 11)])

                advanced_safe = self.advanced_check_safe(board, i, j)
                if advanced_safe != []:
                    for s in advanced_safe:
                        clauses.append([self.var(s[0], s[1], 11)])

        s = Solver()
        for clause in clauses:
            s.add_clause(clause)
        sat, solution = s.solve()
        # print(sat)
        # print(solution)
        return [sat, solution]
