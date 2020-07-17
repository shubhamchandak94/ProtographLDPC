import sys

from TannerGraph import TannerGraph
from RegularLDPC import RegularLDPC
from ProtographLDPC import ProtographLDPC
from Protograph import Protograph


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


def protographLDPC_sandbox():
    points = [[0, 0], [0, 1], [1, 0], [1, 2]]
    protograph = Protograph(points)

    # graph = ProtographLDPC([2, TannerGraph(points)], None)
    protograph_matrix = TannerGraph.get_matrix_representation(protograph.tanner_graph)

    for row in protograph_matrix:
        print(row)

    protographLDPC = ProtographLDPC([protograph, 3], None)
    expanded_matrix = TannerGraph.get_matrix_representation(protographLDPC.tanner_graph)

    print()
    for row in expanded_matrix:
        print(row)


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
    # TannerGraph.analyze(code)
    #
    # code = RegularLDPC([10, 4], "populate-rows")
    # TannerGraph.analyze(code)
    #
    # code = RegularLDPC([10, 4], "populate-columns")
    # TannerGraph.analyze(code)
    #
    # code = RegularLDPC([10, 4, 2], "gallagher")
    # TannerGraph.analyze(code)
    #
    # code = RegularLDPC([10, 4, 2], "populate-rows")
    # TannerGraph.analyze(code)
    #
    # code = RegularLDPC([10, 4, 2], "populate-columns")
    # TannerGraph.analyze(code)
    #
    # code = RegularLDPC([10, 3, 2, False], "gallagher")
    # TannerGraph.analyze(code)
    #
    # code = RegularLDPC([10, 3, 2, False], "populate-rows")
    # TannerGraph.analyze(code)
    #
    # code = RegularLDPC([10, 3, 2, False], "populate-columns")
    # TannerGraph.analyze(code)


    # initialize a protograph
    points = [[0, 0], [0, 1], [1, 0], [1, 2]]
    protograph = Protograph(points)

    protograph_as_matrix = TannerGraph.get_matrix_representation(protograph.tanner_graph)

    for row in protograph_as_matrix:
        print(row)

    protographLDPC = ProtographLDPC([protograph, 2])
    expanded_matrix = TannerGraph.get_matrix_representation(protographLDPC.tanner_graph)

    print()
    for row in expanded_matrix:
        print(row)



ldpcConstructionTests()

#
# protographLDPC_sandbox()
#
# main()