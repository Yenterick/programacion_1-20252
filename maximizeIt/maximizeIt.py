from itertools import product

def solveTuple(values: tuple, m: int) -> int:
    return sum(value**2 for value in values) % m

def maximizeIt(matrix: str) -> int:
    matrix = matrix.split('\n')
    _,m = matrix.pop(0).split(' ')
    matrix = [list(map(int, x.split(' ')[1:])) for x in matrix]
    return max(solveTuple(x, int(m)) for x in product(*matrix))

values = input()
for _ in range(int(values[0])):
    values += '\n' + input()

print(maximizeIt(values))