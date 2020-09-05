import os
import shutil
import argparse
import random
import math

from libs.RegularLDPC import RegularLDPC
from libs.ProtographLDPC import ProtographLDPC
from libs.Protograph import Protograph
from libs.TannerGraph import *


def get_parser():
    # argument parser
    parser = argparse.ArgumentParser(description='Input')
    parser.add_argument('--output-pchk-file', '-o',
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
    parser.add_argument('--code-type', '-t',
                        action='store',
                        dest='code_type',
                        choices=['regular', 'protograph'],
                        help='Type of LDPC code to construct.',
                        required=True)
    parser.add_argument('--construction', '-c',
                        action='store',
                        dest='construction',
                        type=str,
                        default='peg',
                        help='Method used for code construction (default peg). \
                              Other options: regular: \
                              {gallager,populate-rows,populate-columns}.\
                              protograph: {sum-permutations,quasi-cyclic,permuted-quasi-cyclic}.',
                        required=False)
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
    parser.add_argument('--fraction-transmitted', '-f',
                        action='store',
                        dest='fraction_transmitted',
                        type=float,
                        default=1.0,
                        help='For regular codes: fraction of bits out of n-bits \
                             to transmit (randomly chosen). [default: 1.0]')
    parser.add_argument('--protograph-file', '-p',
                        action='store',
                        dest='protograph_file',
                        type=str,
                        help='For protograph codes: file containing protograph.')
    parser.add_argument('--expansion-factor', '-e',
                        action='store',
                        dest='expansion_factor',
                        type=int,
                        help='For protograph codes: protograph expansion factor.')
    parser.add_argument('--seed', '-s',
                        action='store',
                        dest='seed',
                        type=int,
                        help='Random seed for reproducibility. [default: 123]',
                        default=123)
    return parser


# file should be opened with the wb mode
# writes a single value to specified file in binary
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


# writes entire tanner graph in machine readable to specified file
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
Currently, the construction of two different types of
ldpc codes are supported, regular and protograph codes (construction details are laid out in the respective class
files).
'''


def main():
    parser = get_parser()
    args = parser.parse_args()

    # set random seed
    random.seed(args.seed)

    pchk_file = args.pchk_file
    code_type = args.code_type
    construction = args.construction

    protograph = None
    factor = None

    # will write this to disk after population
    ldpc_code = None

    if code_type == "regular":
        if args.n_checks is None or args.n_bits is None or args.checks_per_col is None:
            raise RuntimeError('Please provide n_checks, n_bits and checks_per_col for regular codes.')
        regular_dimension_args = [args.n_bits, args.n_checks, args.checks_per_col]
        ldpc_code = RegularLDPC(regular_dimension_args, construction,
                                verbose=True)  # setting verbose to true prints code info during construction

    elif code_type == "protograph":
        if args.protograph_file is None or args.expansion_factor is None:
            raise RuntimeError('Please provide protograph_file and expansion_factor for protograph codes.')
        protograph_file = args.protograph_file
        factor = args.expansion_factor
        protograph = Protograph(protograph_file)
        ldpc_code = ProtographLDPC(protograph, factor, construction)

    # write the corresponding graph to specified file in binary
    write_graph_to_file(ldpc_code, pchk_file)
    print("INFO: Before puncturing (if applicable):")
    print("INFO: # check nodes =", ldpc_code.height)
    print("INFO: # variable nodes (bits in codeword) =", ldpc_code.width)
    print("INFO: # message bits =", ldpc_code.width - ldpc_code.height)
    print("INFO: # Rate =", "{:.2f}".format((ldpc_code.width - ldpc_code.height) / ldpc_code.width))

    puncturing_used = None
    bits_to_transmit = None
    num_bits_transmitted = None

    # generate .transmitted file for puncturing if needed
    transmitted_bits_file = pchk_file + ".transmitted"

    if code_type == "protograph":
        if protograph.transmitted_bits is not None:  # otherwise no puncturing required

            bits_to_transmit = \
                [j for i in protograph.transmitted_bits for j in range(i * factor, i * factor + factor)]
            num_bits_transmitted = len(bits_to_transmit)
            puncturing_used = True

    elif code_type == "regular":
        assert 0.0 < args.fraction_transmitted <= 1.0
        if args.fraction_transmitted != 1.0:  # otherwise no puncturing required

            num_bits_transmitted = math.ceil(args.fraction_transmitted * ldpc_code.width)

            bits_to_transmit = random.sample(range(ldpc_code.width), num_bits_transmitted)
            bits_to_transmit.sort()
            puncturing_used = True

    if puncturing_used:
        f = open(os.path.join(transmitted_bits_file), 'w')
        f.write('total bits before transmission: ' + str(
            str(ldpc_code.width) + '\n' + ' '.join([str(pos) for pos in bits_to_transmit])))

    print()
    if puncturing_used:
        print("INFO: Puncturing used:")
        print("INFO: # check nodes =", ldpc_code.height)
        print("INFO: # transmitted variable nodes (bits in codeword) =", num_bits_transmitted)
        print("INFO: # message bits =", ldpc_code.width - ldpc_code.height)
        print("INFO: # Rate = ", "{:.2f}".format((ldpc_code.width - ldpc_code.height) / num_bits_transmitted))
    else:
        print("INFO: Puncturing NOT used")


if __name__ == '__main__':
    main()