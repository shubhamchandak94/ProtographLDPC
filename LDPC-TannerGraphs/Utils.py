import random
import os
import sys

# Utils as they relate to graphs

'''
traverses the dictionary to find identical key values. These correspond to repeated parity check equations which
could undermine the code's performance.
'''


def has_repeated_rows(self):
    for i in range(0, len(self.tanner_graph) - 1):
        for j in range(i + 1, len(self.tanner_graph)):
            if self.tanner_graph[i] == self.tanner_graph[j]:
                print("row " + str(i) + " and row " + str(j) + " are identical")
                return True
    return False


'''
the equivalent of transposing a matrix, if that matrix were represented by a bipartite graph. This allows for more
diverse methods of matrix construction.
'''


def transpose(tanner_graph, new_height):
    new_graph = {}
    for i in range(new_height):
        new_graph[i] = []
        for j in tanner_graph:
            if tanner_graph.get(j).count(i) == 1:
                new_graph.get(i).append(j)
    return new_graph


'''
because this program stores ldpc parity information in the form of tanner graphs, this provides a way to construct
the appropriate matrix provided the tanner graph
'''


def get_matrix_representation(tanner_graph):
    matrix = []
    for i in range(len(tanner_graph)):
        row = []
        if i in tanner_graph:
            for j in range(max(tanner_graph[i]) + 1):
                if j in tanner_graph[i]:
                    row.append(1)
                else:
                    row.append(0)
        matrix.append(row)
    normalize(matrix)
    return matrix


def normalize(arr):
    new_length = largest_row(arr)
    for i in range(len(arr)):
        arr[i] = arr[i] + [0] * (new_length - len(arr[i]))


def largest_row(arr):
    largest = 0
    for row in arr:
        if len(row) > largest:
            largest = len(row)
    return largest


# General Utils
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


# display a parity check matrix
def print_matrix(matrix):
    for row in matrix:
        print(row)
