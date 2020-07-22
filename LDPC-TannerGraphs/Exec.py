import sys

from Identity import Identity
from TannerGraph import *
from RegularLDPC import RegularLDPC
from ProtographLDPC import ProtographLDPC
from Protograph import Protograph

from TannerGraph import printm


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


# code which instantiates codes in the correct format
def main():
    # args:
    # pchk-file construction-type [w, h | n, c, r | w, h, c]

    # initializing tanner rep, 2nd argument is construction method
    ldpc_dimension_args = [int(i) for i in sys.argv[3:len(sys.argv)]]

    # create ldpc code
    ldpc_code = RegularLDPC(ldpc_dimension_args, sys.argv[2])

    # write the corresponding graph to specified file in binary
    write_graph_to_file(ldpc_code, sys.argv[1])


'''

Constructions to implement:
Input - Construction

Regular LDPC:
Width, Height - Gallagher, Populate Rows, Populate Columns
Width, Height, 1s per col - Gallagher, Populate Rows, Populate Columns
Width, 1s per col, 1s per row, height provided=false - Gallagher, Populate Rows, Populate Columns
'''


def ldpcConstructionTests():
    # code = RegularLDPC([10, 4], "gallagher")
    # analyze(code)
    #
    # code = RegularLDPC([10, 4], "populate-rows")
    # analyze(code)
    #
    # code = RegularLDPC([10, 4], "populate-columns")
    # analyze(code)
    #
    # code = RegularLDPC([10, 4, 2], "gallagher")
    # analyze(code)
    #
    # code = RegularLDPC([10, 4, 2], "populate-rows")
    # analyze(code)
    #
    # code = RegularLDPC([10, 4, 2], "populate-columns")
    # analyze(code)
    #
    # code = RegularLDPC([10, 3, 2, False], "gallagher")
    # analyze(code)
    #
    # code = RegularLDPC([10, 3, 2, False], "populate-rows")
    # analyze(code)
    #
    # code = RegularLDPC([10, 3, 2, False], "populate-columns")
    # analyze(code)

    # points = [[0, 0, 2], [0, 1, 1], [1, 0, 1], [1, 2, 1]]
    points = [[0, 0, 2], [0, 1, 1], [0, 4, 2], [0, 5, 1], [1, 0, 1], [1, 1, 1], [1, 2, 1], [1, 4, 1], [1, 5, 1],
              [1, 6, 1], [2, 1, 1], [2, 2, 1], [2, 3, 1], [2, 5, 1], [2, 6, 1], [2, 7, 1], [3, 2, 1], [3, 3, 2],
              [3, 6, 1], [3, 7, 2]]

    protograph = Protograph(points)

    protographLDPC = ProtographLDPC([protograph, 3], "quasi-cyclic")
    printm(protographLDPC)

    


ldpcConstructionTests()

#
# protographLDPC_sandbox()
#
# main()
