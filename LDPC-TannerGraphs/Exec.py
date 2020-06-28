import sys

import RegularLDPC
import ProtographLDPC

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
    ldpc_code = RegularLDPC.RegularLDPC(ldpc_dimension_args, sys.argv[2])

    # write the corresponding graph to specified file in binary
    write_graph_to_file(ldpc_code, sys.argv[1])


# a sandbox function for testing ldpc matrix constructions
def sandbox():
    code = RegularLDPC.RegularLDPC([1000, 200], "gallager")
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
