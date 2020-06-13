import random
import sys

'''
- A class for the handling of Regular LDPC matrices in tanner graph form

The tanner graph is stored as a dictionary, row indices (check nodes) are mapped to lists of column indices (variable 
nodes) to indicate bipartite connections

args: input to enable construction. input follows the following construction patern: h = n * (c / r) where c / r is not 
explicitly simplified, h = height of matrix, n = length of codeword/width matrix, c = column weight, r = row weight
where weightages are constant for the most part (certain constructions fail to provide complete regularity)

int construction specifies the method by which the matrix corresponding to args will be created
'''


class RegularLDPC:

    def __init__(self, args, construction):

        self.args = args
        self.width = int(args[0])

        #
        # args provided [width, height]
        # no col weight provided, col weight inferred to preserve regularity of the matrix
        #
        # here, c and r are inferred from the provided width, height values according to the construction equality
        # h = n * (c / r)
        #
        # in the first case, if the gcd of the width and height equals either the width or the height, complete
        # simplification of the fraction yields a situation where either c or r is equal to 1. To counter this effect,
        # if the gcd of the two is equal to one of them, the second gcd is found and c / r is reduced
        # by dividing both c and r by this second gcd. In this way, the greatest sparsity is achieved without resulting
        # in row or col weightages equal to 1.
        #
        if len(args) == 2:

            # if int(args[0]) < int(args[1]):
            #     print("width must be greater than height")
            #     exit()
            #
            # # self.n = int(args[0])
            # #
            # # if gcd(args[0], args[1]) == min(args[0], args[1]) and gcd2(args[0], args[1]) != 1:
            # #
            # #     self.r = int(args[0] / gcd2(args[0], args[1]))
            # #     self.c = int(args[1] / gcd2(args[0], args[1]))
            # #
            # # else:
            # #
            # #     self.r = int(args[0] / gcd(args[0], args[1]))
            # #     self.c = int(args[1] / gcd(args[0], args[1]))
            # #
            # # self.height = int(args[1])
            #
            # w = int(args[0])
            # h = int(args[1])
            #
            # gcf = gcd(w, h)
            #
            # w /= gcf
            # h /= gcf
            #
            # if h < 3:
            #     w *= 3
            #     h *= 3
            #
            # self.n = int(args[0])
            # self.c = int(h)
            # self.r = int(w)
            #
            # self.width = int(args[0])
            # self.height = int(args[1])

            self.width = int(args[0])
            self.height = int(args[1])

            c_f = common_factors(self.width, self.height)
            index = 1

            r = self.width / c_f[len(c_f) - index]
            c = self.height / c_f[len(c_f) - index]

            while (c < 3 or r == 1) and index != len(c_f):
                index += 1

                r = self.width / c_f[len(c_f) - index]
                c = self.height / c_f[len(c_f) - index]

            self.n = int(self.width)
            self.r = int(r)
            self.c = int(c)

        #
        # args provided [width, col weight, row weight, height provided]
        # height inferred given regularity of matrix (fourth argument always false, included to distinguish between
        # args permutations)
        #
        # here, the length of the codeword, the col weight, and the row weight are specified and fed directly into the
        # tanner graph constructor
        #
        elif len(args) == 4:

            self.height = int(args[0] * args[1] / args[1])

            self.n = int(args[0])
            self.c = int(args[1])
            self.r = int(args[2])

        #
        # args provided [width, height, 1s per col]
        # user-controlled matrix weightages
        #
        # here, a value of c is defined along with width and height so that the program does not have to infer the
        # simplicity of (c / r). Because r is dependent on width, height, and c (assuming regularity), defining c results
        # in limiting the constructor to one possible r value. The resulting n, c, r values are passed to the constructor
        #
        elif len(args) == 3:

            self.height = int(args[1])

            self.n = int(args[0])
            self.c = int(args[2])
            self.r = int((self.width / self.height) * self.c)

        else:
            print("invalid input provided")
            return

        self.tanner_graph = RegularLDPC.get_parity_check_graph(self.n, self.r, self.c, construction)

        print("w: " + str(self.width))
        print("h: " + str(self.height))

        # print("n: " + str(self.n))
        print("c: " + str(self.c))
        print("r: " + str(self.r))

    @staticmethod
    def get_parity_check_graph(n, r, c, method):

        # Gallager's construction of random LDPC matrices
        if method == "gallager":

            # keeps track of all created submatrices
            submatrices = []
            for i in range(c):
                # creates random submatrix, appends it to list
                submatrices.append(SubGraph(n, r))

            # merges all matrices in submatrices for final ldpc matrix
            return RegularLDPC.merge(submatrices, n, r)

        # Random construction 1
        # populates columns randomly
        elif method == "random":

            # create base tanner graph with r = 0, c = 0
            tanner_graph = {}
            counts = {}  # stores weight of each row key
            for i in range(int(n * c / r)):
                tanner_graph[i] = []
                counts[i] = 0

            col = 0

            # as columns are traversed, this list maintains the row indices which are still available for population
            available_rows = [i for i in range(int(n * c / r))]

            while len(available_rows) > 0:

                # chooses c random row indices
                col_indices = random_list(available_rows, c)

                # populates tanner graph at chosen indices
                for index in col_indices:
                    tanner_graph[index].append(col)
                    counts[index] += 1

                # removes rows which have reached capacity from available_rows
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

        # ------------------------------------------------
        # Duplicate code included for easier understanding
        # ------------------------------------------------

        # enforces constant row weight
        elif method == "populate-rows":

            # constructs initial empty parity check matrix
            tanner_graph = {}
            for i in range(int(n * c / r)):
                tanner_graph[i] = []

            width = n
            height = int(n * c / r)

            # all possible 1s locations (index in column)
            available_indices = []

            k = n * c
            for i in range(k - 1, -1, -1):
                # fills available indices with column indices
                available_indices.append(i % width)

            placed_entries = 0
            for i in range(height):
                for j in range(r):

                    # loops through all index positions in available indices, stops when the row does not contain a 1 at
                    # a specified index
                    l = 0
                    while l < len(available_indices) and tanner_graph.get(i).count(available_indices[l]) == 1:
                        l += 1

                    # if all entries have been placed
                    if l + placed_entries == k:

                        # choose a random column index and populate the matrix at that location
                        random_index = random.choice(range(width))
                        while tanner_graph.get(i).count(random_index) == 1:
                            random_index = random.choice(range(width))

                        tanner_graph.get(i).append(random_index)

                    # if not all entries have been placed
                    else:

                        # choose a random column index
                        random_index = random.choice(range(len(available_indices)))
                        while tanner_graph.get(i).count(available_indices[random_index]) != 0 and len(
                                available_indices) > 1:
                            random_index = random.choice(range(len(available_indices)))

                        # populate the matrix at specified location
                        tanner_graph.get(i).append(available_indices.pop(random_index))
                        placed_entries += 1

            return tanner_graph

        # enforces constant column weight
        elif method == "populate-columns":

            # create the initial empty graph
            tanner_graph = {}
            for i in range(n):
                tanner_graph[i] = []

            width = n
            height = int(n * c / r)

            # contains all the possible indices for population
            available_indices = []

            k = n * c
            for i in range(k - 1, -1, -1):
                # fills available indices with row indices
                available_indices.append(i % height)

            placed_entries = 0
            for i in range(width):
                for j in range(c):

                    # loops through available entries to find an index that is not already populated
                    l = 0
                    while l < len(available_indices) and tanner_graph.get(i).count(available_indices[l]) == 1:
                        l += 1

                    # if all entries have been placed
                    if placed_entries + l == k:

                        # choose a random row index, not restrained by available indices
                        random_index = random.choice(range(height))
                        while tanner_graph.get(i).count(random_index) == 1:
                            random_index = random.choice(range(height))

                        # populate matrix at that location
                        tanner_graph.get(i).append(random_index)

                    # if not all 1s have been placed
                    else:

                        # choose a random available index
                        random_index = random.choice(range(len(available_indices)))
                        while tanner_graph.get(i).count(available_indices[random_index]) != 0 and len(
                                available_indices) > 1:
                            random_index = random.choice(range(len(available_indices)))

                        # populate matrix at that location
                        tanner_graph.get(i).append(available_indices.pop(random_index))
                        placed_entries += 1

            return RegularLDPC.transpose(tanner_graph, height)

    '''
    as part of the Gallager construction, this function merges all the generated submatrices vertically 
    (in this case sub graphs)
    '''

    @staticmethod
    def merge(submatrices, n, r):
        merged = {}
        for i in range(len(submatrices)):
            for j in range(int(n / r)):
                merged[int(i * n / r + j)] = submatrices[i].map[j]
        return merged

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

    @staticmethod
    def transpose(tanner_graph, new_height):
        new_graph = {}
        for i in range(new_height):
            new_graph[i] = []
            for j in tanner_graph:
                if tanner_graph.get(j).count(i) == 1:
                    new_graph.get(i).append(j)
        return new_graph

    '''
    because this program stores ldpc parity information in the form of a tanner graph, this provides a way to construct
    the appropriate matrix provided the tanner graph
    '''

    @staticmethod
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
        RegularLDPC.normalize(matrix)
        return matrix

    def as_matrix(self):
        return RegularLDPC.get_matrix_representation(self.tanner_graph)

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

    '''
    returns a string which, when the method is run in the context of Radford Neal's library, can be utilized by the 
    make-pchk method to create the appropriate parity check file corresponding to the tanner graph in machine-readable 
    form 
    '''

    # generates a c program call which uses make-ldpc to generate an equivalent ldpc matrix
    def get_c_executable(self, output_file):
        out = "./LDPC-codes/make-pchk " + output_file + " "

        # getting width and height
        if len(self.args) == 2:
            out += str(self.height) + " " + str(self.width) + " "
        elif len(self.args) == 3:
            out += str(self.n) + " " + str(int(self.n * self.c / self.r)) + " "

        # getting all 1s positions
        for i in range(len(self.tanner_graph)):
            for j in range(len(self.tanner_graph[i])):
                out += str(i) + ":" + str(self.tanner_graph[i][j]) + " "

        return out[0:len(out) - 1]


# the equivalent of the submatrix in Gallager's construction
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


# UTILS
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


# writes tanner graph in machine readable to specified file
def write_graph_to_file(ldpc_code, filepath):
    with open(filepath, "wb") as f:

        intio_write(f, (ord('P') << 8) + 0x80)

        intio_write(f, ldpc_code.height)
        intio_write(f, ldpc_code.width)

        for key in ldpc_code.tanner_graph:
            intio_write(f, -(key + 1))
            for value in sorted(ldpc_code.tanner_graph.get(key)):
                intio_write(f, (value + 1))

        intio_write(f, 0)


def main():
    # args:
    # pchk-file construction-type [w, h | n, c, r | w, h, c]

    # initializing tanner rep, 2nd argument is construction method
    ldpc_dimension_args = [int(i) for i in sys.argv[3:len(sys.argv)]]

    # create ldpc code
    ldpc_code = RegularLDPC(ldpc_dimension_args, sys.argv[2])

    # write the corresponding graph to specified file in binary
    write_graph_to_file(ldpc_code, sys.argv[1])


# a sandbox function for testing ldpc matrix constructions
def sandbox():
    code = RegularLDPC([1000, 200], "populate-columns")
    # print(code.tanner_graph)

    matrix = code.as_matrix()
    # for line in matrix:
    #     print(line)

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
# sandbox()
