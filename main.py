from functools import reduce


def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def maplist(f, l):
    if len(l) == 0:
        return []
    return [f(l[0])] + maplist(f, l[1:])


def merge(l1, l2):
    if len(l1) == 0:
        return l2
    return [l1[0]] + merge(l1[1:], l2)


# flatten a list of lists (lol)
def flatten(lol):
    return reduce(merge, lol, [])


def rangelist(n):
    return list(range(n))


def pairrange(i, n):
    return list(map(lambda a: (a, i), range(1, n)))


def flatmap(f, l):
    return flatten(map(f, l))


# given n, find all pairs (i, j) such that 0 <= j < i <= n and i + j is prime. Print the results as (i, j, i+j)
# print(list(map( lambda p: (p[0], p[1], p[0] + p[1]),
#     filter(lambda pair: pair[1] < pair[0] and is_prime(pair[0] + pair[1]),
#                   flatmap(lambda i : list(map(lambda j : (i, j), range(1, i))),
#                           rangelist(7))))))

# This is elegant, but verbose. There might be a cleaner way to write it, by defining a syntactic sugar called collect.

# The Eight Queens Problem
# Find an arrangement on a chess board to place 8 queens such that no queen is attacking others

def is_safe(row, col, queens):
    for queen in queens:
        qr, qc = queen
        # Check if there's a queen in the same row or column
        if qr == row or qc == col:
            return False
        # Check if there's a queen on the same diagonal
        if abs(qr - row) == abs(qc - col):
            return False
    return True


def backtrack(curr_solution, k, solutions):
    if k == 8:
        solutions.append(curr_solution)
    all_pos = pairrange(k, 8 + 1)
    candidates = filter(lambda x: is_safe(x[0], x[1], curr_solution), all_pos)
    # Try to find a solution using one of the candidates
    for pair in candidates:
        backtrack(curr_solution + [pair], k + 1, solutions)
    return None


# But I don't want to backtrack. There is an inordinate concern with time here. We are trying to find one solution,
# going back to fix it, going back to find another solution.
# Rather than backtracking, we can assume that we have all the possible safe combination of queen
# positions till k-1 columns. And then we use that to get all the safe rows for kth column.

def queens(size):
    def fill_cols(k):
        if k == 0:
            return [[]]
        all_possible_before_k = fill_cols(k - 1)
        return flatmap(lambda prev_queens: list(map(lambda valid_pos: prev_queens + [valid_pos],
                                                    list(filter(lambda pos: is_safe(pos[0], pos[1], prev_queens),
                                                                pairrange(k, size+1))))),
                       all_possible_before_k)

    return fill_cols(size)


print(len(queens(8)))

