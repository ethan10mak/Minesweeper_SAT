import random
from sat_solver import sat_solve
from guess import guesser

rows = 16
columns = 30
dim = rows * columns
mine = 9
undiscovered = 10
safe = 11
flag = 12


class setup:
    def __init__(self):
        self.rows = 11
        self.columns = 11
        self.dim = self.rows * self.columns
        self.mine = 9
        self.k_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    def create_empty_board(self, r, c):
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
    def generate_numbers(self, board, r, c):
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

    # Return Board
    def create_board(r, c, n, first, setup):
        if setup != 0:
            pass
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
                sat_solve.solve()
            mines.append([i, j])
