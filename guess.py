# Guessing algorithm that determines the chances of a tile being safe.

from itertools import combinations
from collections import Counter


rows = 16
columns = 30
dim = rows * columns
mine = 9
undiscovered = 10
safe = 11
flag = 12


class guesser:
    def __init__(self):
        self.rows = 11
        self.columns = 11
        self.dim = self.rows * self.columns
        self.mine = 9
        self.k_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    # Checks if the possible mines follow the constraints of the board
    def check_board(board, new_mines):
        for i in range(0, rows):
            for j in range(0, columns):
                state = board[i][j]
                if state != mine and state != undiscovered:
                    mine_count = 0
                    for a in range(-1, 2):
                        for b in range(-1, 2):
                            if (a + i > -1 and a + i < rows) and (
                                b + j > -1 and b + j < columns
                            ):
                                if [a + i, b + j] in new_mines or board[a + i][
                                    b + j
                                ] == flag:
                                    mine_count += 1
                    if mine_count > state:
                        return False
        return True

    # Recursive backtracking algorithm
    def all_combinations(self, board, tiles, mines, count_i, count_j):
        if mines == 0:
            return tiles
        if self.check_board(board, tiles) == False:
            return []
        for i in range(0, rows):
            for j in range(0, columns):
                if i > count_i and j > count_j:
                    old_tiles = []
                    for k in tiles:
                        old_tiles.append(k)

                    if board[i][j] == undiscovered:
                        tiles.append([i, j])
                        check = self.all_combinations(
                            self, board, tiles, mines - 1, i, j
                        )
                        if check != []:
                            return tiles
                    tiles = old_tiles
        return tiles

    def var(i, j):
        if columns < 11:
            return (i * 11 * 11) + (j * 11) + 10
        else:
            return (i * columns * columns) + (j * columns) + 10

    def rev_var(n):
        i = 0
        j = 0
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
        return [i, j]

    # Takes in a list of list of possible mines and returns the safest areas
    def least_frequent(self, l):
        count = dict()
        for i in l:
            for j in i:
                value = self.var(j[0], j[1])
                if value in count.keys():
                    count[value] = count[value] + 1
                else:
                    count.update({value: 1})
        return count

    # Finds a list of the safest tiles on the current board
    def guess_safe(self, board, mines):
        undis_tiles = []
        for i in range(0, rows):
            for j in range(0, columns):
                if board[i][j] == undiscovered:
                    undis_tiles.append([i, j])
        print("Guessing")
        all = []
        start_i = -1
        start_j = -1
        for i in range(0, rows):
            for j in range(0, columns):
                comb = self.all_combinations(self, board, [], mines, start_i, start_j)
                if comb != []:
                    # print("Another:")
                    # print([comb[0][0], comb[0][1]])
                    start_i = comb[0][0]
                    start_j = comb[0][1]
                    all.append(comb)
        frequency = self.least_frequent(self, all)
        safest = -1
        current = -1
        for i in frequency.keys():
            if current == -1:
                current = frequency[i]
                safest = i
            if frequency[i] < safest:
                current = frequency[i]
                safest = i
        return self.rev_var(safest)
