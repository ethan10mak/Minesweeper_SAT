from sat_solver import sat_solve
from guess import guesser
from board import board
import time


def run_multiple(n):
    win = 0
    lose = 0
    for i in range(0, n):
        result = board.play(8, 15, True, -1)
        if result == "Win":
            win += 1
        else:
            lose += 1
    print([win, lose])
    return [win, lose]


# board.play(8, 15, True)
# Calculate the start time
start = time.time()

# Code here

# Calculate the end time and time taken

result = run_multiple(50)
print("Win:")
print(result[0])

print("Lose:")
print(result[1])
end = time.time()
length = end - start

print("Time:")
print(length)

# 2
# 8

# 2
# 8

# 5
# 5

# 3
# 7

# 20
# 80
