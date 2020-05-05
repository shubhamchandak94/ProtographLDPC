import random
import sys


# the equivalent of the submatrix in Gallagher's construction
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


# because of recurring integer division, no warning is given if provided (n, r) configuration is unattainable
class RegularLDPC:

    def __init__(self, args):

        self.args = args

        # order provided: w, h
        if len(args) == 2:

            if RegularLDPC.gcd(args[0], args[1]) == min(args[0], args[1]) and RegularLDPC.gcd2(args[0], args[1]) != 1:
                self.tanner_graph = RegularLDPC.get_parity_check_graph(args[0], int(
                    args[0] / RegularLDPC.gcd2(args[0], args[1])), int(args[1] / RegularLDPC.gcd2(args[0], args[1])))
            else:
                self.tanner_graph = RegularLDPC.get_parity_check_graph(args[0],
                                                                       int(args[0] / RegularLDPC.gcd(args[0], args[1])),
                                                                       int(args[1] / RegularLDPC.gcd(args[0], args[1])))

        # order provided: n, c, r
        elif len(args) == 3:
            self.tanner_graph = RegularLDPC.get_parity_check_graph(args[0], args[2], args[1])
        else:
            return

    def get_matrix_representation(self):
        matrix = []
        for i in range(len(self.tanner_graph)):
            row = []
            for j in range(max(self.tanner_graph[i]) + 1):
                if j in self.tanner_graph[i]:
                    row.append(1)
                else:
                    row.append(0)
            matrix.append(row)
        RegularLDPC.normalize(matrix)
        return matrix

    def get_c_executable(self, output_file):
        out = "./LDPC-codes/make-pchk " + output_file + " "

        # getting width and height
        if len(self.args) == 2:
            out += str(self.args[1]) + " " + str(self.args[0]) + " "
        elif len(self.args) == 3:
            out += str(self.args[0]) + " " + str(int(self.args[0] * self.args[1] / self.args(2))) + " "

        # getting all 1s positions
        for i in range(len(self.tanner_graph)):
            for j in range(len(self.tanner_graph[i])):
                out += str(i) + ":" + str(self.tanner_graph[i][j]) + " "

        return out[0:len(out) - 1]

    @staticmethod
    def get_parity_check_graph(n, r, c):
        submatrices = []
        for i in range(c):
            submatrices.append(SubGraph(n, r))
        return RegularLDPC.merge(submatrices, n, r)

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


try:
    # parsing arguments
    ldpc_args = [int(i) for i in sys.argv[2:len(sys.argv)]]

    ldpcCode = RegularLDPC(ldpc_args)
    # print(ldpcCode.get_c_executable(sys.argv[1]))

    f = open("transfer.txt", "w")
    f.write(ldpcCode.get_c_executable(sys.argv[1]))
    f.close()
except:
    print("Usage: MakePCHKT parity-check-file [width, height | codeword legnth, 1s per col, 1s per row]")
