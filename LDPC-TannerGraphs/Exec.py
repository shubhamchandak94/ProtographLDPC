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
    if isinstance(ldpc_code, Protograph):
        print("cannot write Protographs to disk in raw form, must convert to an ldpc code")
        return

    with open(filepath, "wb") as f:

        intio_write(f, (ord('P') << 8) + 0x80)

        intio_write(f, ldpc_code.height)
        intio_write(f, ldpc_code.width)

        for key in ldpc_code.tanner_graph:
            intio_write(f, -(key + 1))
            for value in sorted(ldpc_code.tanner_graph.get(key)):
                intio_write(f, (value + 1))

        intio_write(f, 0)


'''
This function allows Exec.py to be run from the command line. Currently, the construction of two different types of 
ldpc codes are supported, regular and protograph codes (construction details are laid out in the respective class
files). 
'''


# parameters:
#   args: list, arguments by which the code is to be constructed.
#       format: pchk-file code-type construction args:([w, h | n, c, r | w, h, c], [protograph-file, l])
#   return:
#       None, constructs machine-readable ldpc code in the specified parity check file. The generated format is readable
#       by executables belonging to the LDPC-codes submodule
def main():
    ldpc_code = None

    if sys.argv[2] == "regular":
        # initializing tanner rep, 2nd argument is construction method
        ldpc_dimension_args = [int(i) for i in sys.argv[4:len(sys.argv)]]

        # create regular code
        ldpc_code = RegularLDPC(ldpc_dimension_args, sys.argv[3])

    elif sys.argv[2] == "protograph":

        ldpc_args = [i for i in sys.argv[4:len(sys.argv)]]

        for i in range(len(ldpc_args)):
            try:
                ldpc_args[i] = int(ldpc_args[i])
            except:
                continue

        protograph = Protograph([ldpc_args[0]])

        ldpc_code = ProtographLDPC([protograph, ldpc_args[1]], sys.argv[3], width_provided=True)

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
    # points = [[0, 0, 2], [0, 1, 1], [0, 4, 2], [0, 5, 1], [1, 0, 1], [1, 1, 1], [1, 2, 1], [1, 4, 1], [1, 5, 1],
    #           [1, 6, 1], [2, 1, 1], [2, 2, 1], [2, 3, 1], [2, 5, 1], [2, 6, 1], [2, 7, 1], [3, 2, 1], [3, 3, 2],
    #           [3, 6, 1], [3, 7, 2]]

    # protograph = Protograph(points)

    protograph = Protograph(['../example-protographs/protograph1'])
    # printm(protograph)

    protographLDPC = ProtographLDPC([protograph, 64], "quasi-cyclic", width_provided=True)
    printm(protographLDPC)


# ldpcConstructionTests()

main()
#