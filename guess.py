# Guessing algorithm that determines the chances of a tile being safe.

from itertools import combinations
from collections import Counter
import random

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

    # returns all combinations of mines
    def freq(self, board):
        count = dict()
        for i in range(0, rows):
            for j in range(0, columns):
                temp = []
                if board[i][j] in [1, 2, 3, 4, 5, 6, 7, 8]:
                    mine_count = 0
                    un_count = 0
                    for a in range(-1, 2):
                        for b in range(-1, 2):
                            if (a + i > -1 and a + i < rows) and (
                                b + j > -1 and b + j < columns
                            ):
                                if board[a + i][b + j] == undiscovered and (
                                    a != 0 and b != 0
                                ):
                                    un_count += 1
                                    temp.append([a + i, b + j])
                                elif board[a + i][b + j] == flag:
                                    mine_count += 1
                    else:
                        prob = board[i][j] - mine_count
                    if prob != 0:
                        for x in temp:
                            value = self.var(x[0], x[1])
                            if value in count.keys():
                                count[value] = count[value] + ((prob) / un_count) * 2
                            else:
                                count.update({value: (prob) / un_count})
        return count

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

    # New Idea, make the combinations return the combinations of safe spaces
    # Least frequent will then return the frequency of the safe spaces instead of
    # mine spaces
    # Finds a list of the safest tiles on the current board
    def guess_safe(self, board, mines):
        undis_tiles = []
        for i in range(0, rows):
            for j in range(0, columns):
                if board[i][j] == undiscovered:
                    undis_tiles.append([i, j])
        print("Guessing")
        frequency = self.freq(self, board)
        if frequency == {}:
            random.seed()
            return undis_tiles[random.randint(0, len(undis_tiles) - 1)]
        print(frequency)
        safest = -1
        current = -1
        for i in frequency.keys():
            if current == -1:
                current = frequency[i]
                safest = i
            if frequency[i] < current:
                current = frequency[i]
                safest = i
        lowest_list = []
        for i in frequency.keys():
            if current == frequency[i]:
                print(self.rev_var(i))
                lowest_list.append(i)
        random.seed()
        safest = lowest_list[random.randint(0, len(lowest_list) - 1)]
        print(self.rev_var(safest))
        print(current)
        return self.rev_var(safest)
