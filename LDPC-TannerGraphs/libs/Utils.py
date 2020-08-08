import random
import os
import sys

# GENERAL UTILS
# finds all common factors between i an dj
def common_factors(i, j):
    factors = []
    for z in range(min(i, j) - 1):
        if i % (z + 1) == 0 and j % (z + 1) == 0:
            factors.append(z + 1)
    return factors


# finds the second greatest common denominator for the provided integers
def gcd2(i, j):
    c_f = common_factors(i, j)
    return c_f[len(c_f) - 1]


# finds the greatest common denominator of two integers
def gcd(i, j):
    return gcdr(i, j, min(i, j))


# utilizes a recursive shortcut to find the greatest common denominator quickly
def gcdr(i, j, previous_remainder):
    remainder = max(i, j) % min(i, j)
    # multiplier = (max(i, j) - remainder) / min(i, j);

    if remainder == 0:
        return previous_remainder
    else:
        return gcdr(min(i, j), remainder, remainder)


# chooses random n elements from to_pass, does not alter passed args
def random_list(list, n):
    to_pass = list.copy()
    return rand_list(to_pass, n, [])


# choose random n elements from list, selected always entered as []: alters arguments
def rand_list(list, n, selected):
    if n == 0 or len(list) == 0:
        return selected
    else:
        randint = random.choice(list)
        selected.append(randint)
        list.remove(randint)
        return rand_list(list, n - 1, selected)