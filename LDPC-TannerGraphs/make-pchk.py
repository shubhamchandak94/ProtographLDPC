import os
import sys
import shutil

from libs.RegularLDPC import RegularLDPC
from libs.ProtographLDPC import ProtographLDPC
from libs.Protograph import Protograph

from libs.TannerGraph import printm


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
This function allows exec.py to be run from the command line. Currently, the construction of two different types of
ldpc codes are supported, regular and protograph codes (construction details are laid out in the respective class
files).
'''


# parameters:
#   args: list, arguments by which the code is to be constructed.
#       format: pchk-file code-type construction ([w, h | n, c, r, x | w, h, c], [protograph-dir, factor])
#           if code-type == regular
#
#               row column weights inferred
#               1) w: width of code
#                  h: height of code
#
#               height inferred
#               2) n: width of code
#                  c: weight of columns
#                  r: weight of rows
#                  x: random number (has no pertinence to the construction, just to distinguish between possible arguments
#
#               row weightage inferred
#               3) w: width of code
#                  h: height of code
#                  c: column weightage
#
#           if code-type == protograph
#               protograph-dir: path to protograph file
#               factor: expansion factor
#
#   return:
#       None, constructs machine-readable ldpc code in the specified parity check file. The generated parity check file is
#       readable by executables belonging to the LDPC-codes submodule
def main():
    pchk_file = sys.argv[1]
    code_type = sys.argv[2]
    construction = sys.argv[3]

    args = sys.argv[4:]

    protograph_file = None
    factor = None

    # will write this to disk after population
    ldpc_code = None

    if code_type == "regular":

        regular_dimension_args = [int(i) for i in args]
        ldpc_code = RegularLDPC(regular_dimension_args, construction)

    elif code_type == "protograph":

        protograph_file = args[0]
        factor = int(args[1])

        protograph = Protograph([protograph_file])
        ldpc_code = ProtographLDPC([protograph, factor], construction)

    # determine build paths
    ldpc_filename = os.path.basename(pchk_file)
    ldpc_dir = os.path.join(os.path.dirname(pchk_file), ldpc_filename)

    # if a directory already exists at this path, delete it
    if os.path.isdir(ldpc_dir):
        delete = input("a directory exists at this location, replace? [y/n]: ")
        if delete == 'y':
            shutil.rmtree(ldpc_dir)
        else:
            exit()

    # create ldpc directory
    try:
        os.mkdir(ldpc_dir)
    except FileExistsError:
        print("a code already exists at the specified location")
        return

    # write the corresponding graph to specified file in binary
    ldpc_pchk_file = os.path.join(ldpc_dir, ldpc_filename)
    write_graph_to_file(ldpc_code, ldpc_pchk_file)

    # generate .transmitted file for puncturing if a protograph code is constructed
    if code_type == "protograph":

        contents = open(protograph_file, 'r').read().split('\n')

        protograph_bits_transmitted = [int(i) for i in contents[1].split(' ')[1:]]
        all_transmitted_bits = []

        for i in protograph_bits_transmitted:
            for j in range(i * factor, i * factor + factor):
                all_transmitted_bits.append(str(j))

        f = open(os.path.join(ldpc_dir, '.transmitted'), 'w')
        f.write('factor: ' + str(factor) + '\n' + 'total bits before transmission: ' + str(
            int(contents[0].split(' ')[1]) * factor) + '\n' + ' '.join(all_transmitted_bits))

    elif code_type == "regular":

        f = open(os.path.join(ldpc_dir, '.transmitted'), 'w')
        f.write('factor: None' + '\n' + 'total bits before transmission: ' + str(ldpc_code.width) + '\n' + str(
            list(range(0, ldpc_code.width))).replace(',', '').replace('[', '').replace(']', ''))


# testing sandbox
def ldpcConstructionTests():
    protograph = Protograph(['../protographs/protograph3'])
    printm(protograph)


# ldpcConstructionTests()
#
main()
