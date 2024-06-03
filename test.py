from itertools import combinations

perm = combinations([[1, 2], [2, 3], [1, 1]], 2)

# Print the obtained permutations

for i in list(perm):
    print(i)
