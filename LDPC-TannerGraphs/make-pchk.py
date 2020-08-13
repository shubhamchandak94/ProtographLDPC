import os
import sys
import shutil
import argparse

from libs.RegularLDPC import RegularLDPC
from libs.ProtographLDPC import ProtographLDPC
from libs.Protograph import Protograph


def get_parser():
    # argument parser
    parser = argparse.ArgumentParser(description='Input')
    parser.add_argument('--output-pchk-file','-o',
                        action='store',
                        dest='pchk_file',
                        type=str,
                        help='File to store generated pchk file.\
                        An additional .transmitted file is also generated when \
                        puncturing is used.\
                        For example, when this argument is my.pchk, \
                        then my.pchk.transmitted will also be generated when \
                        puncturing is used.',
                        required=True)
    parser.add_argument('--code-type','-t',
                        action='store',
                        dest='code_type',
                        choices=['regular','protograph'],
                        help='Type of LDPC code to construct.',
                        required=True)
    parser.add_argument('--construction','-c',
                        action='store',
                        dest='construction',
                        type=str,
                        help='Method used for code construction. \
                              Allowed options: regular: \
                              {gallager,random,populate-rows,populate-columns}.\
                              protograph: {permutation,regular,quasi-cyclic,permuted-quasi-cyclic}.',
                        required=True)
    parser.add_argument('--n-checks',
                        action='store',
                        dest='n_checks',
                        type=int,
                        help='For regular codes: number of check nodes.')
    parser.add_argument('--n-bits',
                        action='store',
                        dest='n_bits',
                        type=int,
                        help='For regular codes: number of codeword bits \
                              (including untransmitted/punctured bits).')
    parser.add_argument('--checks-per-col',
                        action='store',
                        dest='checks_per_col',
                        type=int,
                        default=3,
                        help='For regular codes: number of 1s per column of parity \
                             check matrix. [default: 3]')
    parser.add_argument('--fraction-tranmitted','-f',
                        action='store',
                        dest='fraction_tranmitted',
                        type=float,
                        default=1.0,
                        help='For regular codes: fraction of bits out of n-bits \
                             to transmit (randomly chosen). [default: 1.0]')
    parser.add_argument('--protograph-file','-p',
                        action='store',
                        dest='protograph_file',
                        type=str,
                        help='For protograph codes: file containing protograph.')
    parser.add_argument('--expansion-factor','-e',
                        action='store',
                        dest='expansion_factor',
                        type=int,
                        help='For protograph codes: protograph expansion factor.')
    parser.add_argument('--seed','-s',
                        action='store',
                        dest='seed',
                        type=int,
                        help='Random seed for reproducibility. [default: 123]',
                        default=123)
    return parser

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
#       format: pchk-file code-type construction ([w, h, c], [protograph-dir, factor])
#           if code-type == regular
#               row weightage inferred
#                  w: width of code
#                  h: height of code
#                  c: column weightage
#                  f: fraction of bits out of w to transmit (puncturing), default 1.0
#           if code-type == protograph
#               protograph-file: path to protograph file
#               factor: expansion factor
#
#   return:
#       None, constructs machine-readable ldpc code in the specified parity check file. The generated parity check file is
#       readable by executables belonging to the LDPC-codes submodule
def main():
    parser = get_parser()
    args = parser.parse_args()

    pchk_file = args.pchk_file
    code_type = args.code_type
    construction = args.construction

    protograph_file = None
    factor = None

    # will write this to disk after population
    ldpc_code = None

    if code_type == "regular":
         if args.n_checks is None or args.n_bits is None or args.checks_per_col is None:
             raise RuntimeError('Please provide n_checks, n_bits and checks_per_col for regular codes.')
             sys.exit(1)
        regular_dimension_args = [args.n_bits,args.n_checks,args.checks_per_col]
        ldpc_code = RegularLDPC(regular_dimension_args, construction)
    elif code_type == "protograph":
        if args.protograph_file is None or args.expansion_factor is None:
            raise RuntimeError('Please provide protograph_file and expansion_factor for protograph codes.')
        protograph_file = args.protograph_file
        factor = args.expansion_factor
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


if __name__ == '__main__':
    main()
