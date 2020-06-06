import random
import sys
import os

# the equivalent of the submatrix in Gallagher's construction
import time


class SubGraph:

    def __init__(self, n, r):

        # creates graph with appropriate no. check nodes
        self.map = {}
        for i in range(int(n / r)):
            self.map[i] = []

        # defines all possible indices, randomizes for sparse parity-codeword mapping
        codeword_indices = list(range(0, n))
        random.shuffle(codeword_indices)

        # assigns codeword bits to parity check equations
        for i in range(int(n / r)):
            for j in range(int(r)):
                self.map[i].append(codeword_indices[i * r + j])

    def __repr__(self):
        return str(self.map)


# because of recurring integer division, no warning is given if provided (n, r) configuration is unattainable due to
# the nature of each construction that the width is significantly greater than the height of the matrix rep,
# repeated rows are not a concern
class RegularLDPC:

    def __init__(self, args, construction):

        self.args = args

        # order provided: w, h
        if len(args) == 2:
            if RegularLDPC.gcd(args[0], args[1]) == min(args[0], args[1]) and RegularLDPC.gcd2(args[0], args[1]) != 1:
                self.tanner_graph = RegularLDPC.get_parity_check_graph(args[0], int(
                    args[0] / RegularLDPC.gcd2(args[0], args[1])), int(args[1] / RegularLDPC.gcd2(args[0], args[1])),
                                                                       construction)

                self.c = int(args[0] / RegularLDPC.gcd2(args[0], args[1]))
                self.r = int(args[1] / RegularLDPC.gcd2(args[0], args[1]))

            else:
                self.tanner_graph = RegularLDPC.get_parity_check_graph(args[0],
                                                                       int(args[0] / RegularLDPC.gcd(args[0], args[1])),
                                                                       int(args[1] / RegularLDPC.gcd(args[0], args[1])),
                                                                       construction)

                self.c = int(args[0] / RegularLDPC.gcd(args[0], args[1]))
                self.r = int(args[1] / RegularLDPC.gcd(args[0], args[1]))

            self.width = int(args[0])
            self.height = int(args[1])

            self.n = args[0]

        # order provided: n, c, r
        elif len(args) == 3:
            self.tanner_graph = RegularLDPC.get_parity_check_graph(args[0], args[2], args[1], construction)

            self.width = int(args[0])
            self.height = int(args[0] * args[1] / args[1])

            self.n = args[0]
            self.c = args[1]
            self.r = args[2]

        # incorrect args provided
        else:
            return

    @staticmethod
    def get_matrix_representation(tanner_graph):
        matrix = []
        for i in range(len(tanner_graph)):
            row = []
            for j in range(max(tanner_graph[i]) + 1):
                if j in tanner_graph[i]:
                    row.append(1)
                else:
                    row.append(0)
            matrix.append(row)
        RegularLDPC.normalize(matrix)
        return matrix

    # generates a c program call which uses make-ldpc to generate an equivalent ldpc matrix
    def get_c_executable(self, output_file):
        out = "./LDPC-codes/make-pchk " + output_file + " "

        # getting width and height
        if len(self.args) == 2:
            out += str(self.args[1]) + " " + str(self.args[0]) + " "
        elif len(self.args) == 3:
            out += str(self.args[0]) + " " + str(int(self.args[0] * self.args[1] / self.args[2])) + " "

        # getting all 1s positions
        for i in range(len(self.tanner_graph)):
            for j in range(len(self.tanner_graph[i])):
                out += str(i) + ":" + str(self.tanner_graph[i][j]) + " "

        return out[0:len(out) - 1]

    def has_repeated_rows(self):
        for i in range(0, len(self.tanner_graph) - 1):
            for j in range(i + 1, len(self.tanner_graph)):
                if self.tanner_graph[i] == self.tanner_graph[j]:
                    print("row " + str(i) + " and row " + str(j) + " are identical")
                    return True
        return False

    @staticmethod
    def get_parity_check_graph(n, r, c, method):

        if method == "gallager":
            submatrices = []
            for i in range(c):
                submatrices.append(SubGraph(n, r))
            return RegularLDPC.merge(submatrices, n, r)

        elif method == "random":
            # create base tanner graph
            tanner_graph = {}
            counts = {}  # stores weight of each row key
            for i in range(int(n * c / r)):
                tanner_graph[i] = []
                counts[i] = 0

            col = 0
            available_rows = [i for i in range(int(n * c / r))]  # keeps track of which rows can increase weightage
            while len(available_rows) > 0:

                col_indices = random_list(available_rows, c)

                for index in col_indices:
                    tanner_graph[index].append(col)
                    counts[index] += 1

                indices = []
                for index in counts:
                    if counts[index] == r:
                        available_rows.remove(index)
                        indices.append(index)

                # separated to avoid io error with dict operations
                for index in indices:
                    del counts[index]

                col += 1
            return tanner_graph

        # enforces constant column weight
        elif method == "populate-rows":

            tanner_graph = {}
            for i in range(int(n * c / r)):
                tanner_graph[i] = []

            width = n
            height = int(n * c / r)

            # all possible 1s locations (index in column)
            available_indices = []

            k = n * c
            for i in range(k - 1, -1, -1):
                available_indices.append(i % width)

            placed_entries = 0
            for i in range(height):
                for j in range(r):

                    l = 0
                    while l < len(available_indices) and tanner_graph.get(i).count(available_indices[l]) == 1:
                        l += 1

                    if l + placed_entries == k:

                        random_index = random.choice(range(width))
                        while tanner_graph.get(i).count(random_index) == 1:
                            random_index = random.choice(range(width))

                        tanner_graph.get(i).append(random_index)

                    else:
                        random_index = random.choice(range(len(available_indices)))
                        while tanner_graph.get(i).count(available_indices[random_index]) != 0 and len(
                                available_indices) > 1:
                            random_index = random.choice(range(len(available_indices)))

                        tanner_graph.get(i).append(available_indices.pop(random_index))
                        placed_entries += 1

            return tanner_graph
            # return RegularLDPC.enforce_c(tanner_graph, n, c)

        # enforces constant column weight
        elif method == "populate-columns":

            tanner_graph = {}
            for i in range(n):
                tanner_graph[i] = []

            width = n
            height = int(n * c / r)

            available_indices = []
            k = n * c
            for i in range(k - 1, -1, -1):
                available_indices.append(i % height)

            placed_entries = 0
            for i in range(width):
                for j in range(c):

                    l = 0
                    while l < len(available_indices) and tanner_graph.get(i).count(available_indices[l]) == 1:
                        l += 1

                    if placed_entries + l == k:

                        random_index = random.choice(range(height))
                        while tanner_graph.get(i).count(random_index) == 1:
                            random_index = random.choice(range(height))

                        tanner_graph.get(i).append(random_index)

                    else:
                        random_index = random.choice(range(len(available_indices)))
                        while tanner_graph.get(i).count(available_indices[random_index]) != 0 and len(
                                available_indices) > 1:
                            random_index = random.choice(range(len(available_indices)))

                        tanner_graph.get(i).append(available_indices.pop(random_index))
                        placed_entries += 1

            return RegularLDPC.enforce_c(RegularLDPC.transpose(tanner_graph, height), n, c)

    @staticmethod
    def transpose(tanner_graph, new_height):
        new_graph = {}
        for i in range(new_height):
            new_graph[i] = []
            for j in tanner_graph:
                if tanner_graph.get(j).count(i) == 1:
                    new_graph.get(i).append(j)
        return new_graph

    @staticmethod
    def enforce_c(tanner_graph, n, c):

        for col in range(n):

            count = 0
            for row in tanner_graph:
                if tanner_graph.get(row).count(col) == 1:
                    count += 1

            if count < c:
                needed = c - count

                available_indices = []
                for row in tanner_graph:
                    if tanner_graph.get(row).count(col) == 0:
                        available_indices.append(row)

                chosen = random_list(available_indices, needed)
                for row in chosen:
                    tanner_graph.get(row).append(col)

        return tanner_graph

    @staticmethod
    def merge(submatrices, n, r):
        merged = {}
        for i in range(len(submatrices)):
            for j in range(int(n / r)):
                merged[int(i * n / r + j)] = submatrices[i].map[j]
        return merged

    @staticmethod
    def gcd2(i, j):
        factors = []
        for z in range(min(i, j) - 1):
            if i % (z + 1) == 0 and j % (z + 1) == 0:
                factors.append(z + 1)
        return factors[len(factors) - 1]

    @staticmethod
    def gcd(i, j):
        return RegularLDPC.gcdr(i, j, min(i, j))

    @staticmethod
    def gcdr(i, j, previous_remainder):

        remainder = max(i, j) % min(i, j)
        # multiplier = (max(i, j) - remainder) / min(i, j);

        if remainder == 0:
            return previous_remainder
        else:
            return RegularLDPC.gcdr(min(i, j), remainder, remainder)

    @staticmethod
    def normalize(arr):

        new_length = RegularLDPC.largest_row(arr)
        for i in range(len(arr)):
            arr[i] = arr[i] + [0] * (new_length - len(arr[i]))

    @staticmethod
    def largest_row(arr):

        largest = 0
        for row in arr:
            if len(row) > largest:
                largest = len(row)
        return largest


# UTILS
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


# file should be opened with the wb mode
def intio_write(file, value):
    for i in range(3):
        b = value & 0xff

        bAsBinary = int(str(bin(b)), 2)
        binaryBtoBytes = bAsBinary.to_bytes(1, 'little')

        file.write(binaryBtoBytes)

        value >>= 8

    if value > 0:
        b = value
    else:
        b = (value + 256) % 256

    bAsBinary = int(str(bin(b)), 2)
    binaryBtoBytes = bAsBinary.to_bytes(1, 'little')
    file.write(binaryBtoBytes)


def main():
    # global construction_type
    #
    # # initializing tanner rep, 2nd argument is construction method
    # ldpc_dimension_args = [int(i) for i in sys.argv[3:len(sys.argv)]]
    # # if sys.argv[2] == "gallager":
    # #     construction_type = 1
    # # elif sys.argv[2] == "random":
    # #     construction_type = 2
    # # elif sys.argv[2] == "evenboth":
    # #     construction_type = 3
    # # elif sys.argv[2]
    #
    # # ldpcCode = RegularLDPC(ldpc_dimension_args, construction_type)
    # ldpcCode = RegularLDPC(ldpc_dimension_args, sys.argv[2])
    #
    # with open(sys.argv[1], "wb") as f:
    #
    #     intio_write(f, (ord('P') << 8) + 0x80)
    #
    #     intio_write(f, ldpcCode.height)
    #     intio_write(f, ldpcCode.width)
    #
    #     for key in ldpcCode.tanner_graph:
    #         intio_write(f, -(key + 1))
    #         for value in sorted(ldpcCode.tanner_graph.get(key)):
    #             intio_write(f, (value + 1))
    #
    #     intio_write(f, 0)

    matrix = RegularLDPC.get_matrix_representation(code.tanner_graph)

    for line in matrix:
        print(line)

    row_weights = []
    for line in matrix:
        row_weights.append(line.count(1))

    col_weights = []
    for c in range(len(matrix[0])):

        col_weight = 0
        for r in range(len(matrix)):
            if matrix[r][c] == 1:
                col_weight += 1

        col_weights.append(col_weight)

    row_weights = list(dict.fromkeys(row_weights))
    col_weights = list(dict.fromkeys(col_weights))

    if len(row_weights) == 1:
        print("row weight constant")
    else:
        print("row weight not constant")

    if len(col_weights) == 1:
        print("col weight constant")
    else:
        print("col weight not constant")


main()
