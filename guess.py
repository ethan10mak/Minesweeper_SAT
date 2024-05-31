# Guessing algorithm that determines the chances of a tile being safe.

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

    # Finds a list of the safest tiles on the current board
    def guess_safe(board, mines):

        return 0
