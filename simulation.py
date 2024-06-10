from sat_solver import sat_solve
from guess import guesser
from board import board


def run_multiple(n):
    win = 0
    lose = 0
    for i in range(0, n):
        result = board.play(8, 15, True)
        if result == "Win":
            win += 1
        else:
            lose += 1
    return [win, lose]


# board.play(8, 15, True)

result = run_multiple(1)
print("Win:")
print(result[0])

print("Lose:")
print(result[1])

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
