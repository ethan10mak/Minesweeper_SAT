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

    # Checks if the possible mines follow the constraints of the board
    def check_board(board, new_mines, completed):
        for i in range(0, rows):
            for j in range(0, columns):
                state = board[i][j]
                if state != mine and state != undiscovered and state != flag:
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
                    if completed == False and mine_count > state:
                        return False
                    elif completed == True and mine_count != state:
                        return False
                    # if mine_count > state:
                    #   return False
        return True

    """
    # Recursive backtracking algorithm
        """
    """
    def all_combinations(self, board, tiles, mines, count_i, count_j):
        if mines == 0:
            if self.check_board(board, tiles, True):
                return tiles
            return []
        if self.check_board(board, tiles, False) == False:
            return []
        for i in range(0, rows):
            if i >= count_i:
                for j in range(0, columns):
                    if (i == count_i and j > count_j) or (i > count_i):
                        old_tiles = []
                        for k in tiles:
                            old_tiles.append(k)

                        if board[i][j] == undiscovered:
                            tiles.append([i, j])
                            check = []
                            if self.check_board(board, tiles, False):
                                check = self.all_combinations(
                                    self, board, tiles, mines - 1, i, j
                                )
                            if check != []:
                                print("Check")
                                return tiles
                        print(tiles)
                        tiles = old_tiles
        return tiles
    """

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
                    prob = board[i][j] - mine_count
                    if prob != 0:
                        for x in temp:
                            value = self.var(x[0], x[1])
                            if value in count.keys():
                                count[value] = count[value] + (prob * prob)
                            else:
                                count.update({value: (prob * prob)})
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

    # Takes in a list of list of possible mines and returns the frequency of the mines
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
        all = []
        start_i = -1
        start_j = -1
        comb = [1]
        """
        while comb != []:
            comb = self.all_combinations(self, board, [], mines, start_i, start_j)
            print(comb)
            if comb != []:
                # print("Another:")
                # print([comb[0][0], comb[0][1]])
                start_i = comb[0][0]
                start_j = comb[0][1]
                all.append(comb)
        print(all)
        """
        frequency = self.freq(self, board)
        if frequency == []:
            random.seed()
            return undis_tiles[random.randint(0, len(undis_tiles) - 1)]
        print(frequency)
        # frequency = self.least_frequent(self, all)
        safest = -1
        current = -1
        # print(frequency)
        for i in frequency.keys():
            # print(self.rev_var(i))
            # print(frequency[i])
            if current == -1:
                current = frequency[i]
                safest = i
            if frequency[i] < current:
                current = frequency[i]
                safest = i
        lowest_list = []
        # print(self.rev_var(safest))
        # lowest_list.append(safest)
        for i in frequency.keys():
            # print(frequency[i])
            if current == frequency[i]:
                print(self.rev_var(i))
                lowest_list.append(i)
        random.seed()
        safest = lowest_list[random.randint(0, len(lowest_list) - 1)]
        print(self.rev_var(safest))
        print(current)
        return self.rev_var(safest)
