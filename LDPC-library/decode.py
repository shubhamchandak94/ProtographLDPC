import os
import tempfile
import subprocess

import math
import argparse


def get_parser():
    # argument parser
    parser = argparse.ArgumentParser(description='Input')
    parser.add_argument('--pchk-file', '-p',
                        action='store',
                        dest='pchk_file',
                        type=str,
                        help='Parity check file.\
                        An additional .transmitted file should be present when \
                        puncturing is being used.\
                        For example, when this argument is my.pchk, \
                        then the program will search for my.pchk.transmitted \
                         and use it for puncturing if avilable.',
                        required=True)
    parser.add_argument('--received-file', '-i',
                        action='store',
                        dest='received_file',
                        type=str,
                        help='Received file containing one or more blocks (one per line).',
                        required=True)
    parser.add_argument('--output-file', '-o',
                        action='store',
                        dest='output_file',
                        type=str,
                        help='Output file to store decoded blocks (one per line). \
                        An additional output_file.unpunctured is generated when puncturing is used \
                        and contains all the codeword bits including punctured bits, to enable easy \
                        extraction of message bits from the codeword.',
                        required=True)
    parser.add_argument('--channel',
                        action='store',
                        dest='channel',
                        choices={'bsc', 'awgn', 'misc'},
                        help='Channel for computing LLR. Supported options: \
                        binary symmetric channel, \
                        additive white gaussian noise channel (modulation: 0 -> -1, 1 -> +1), \
                        miscellaneous channel (for general channels, input is \
                        LLRs (log-likelihood ratios) as space separated quantities).',
                        required=True)
    parser.add_argument('--channel-parameters',
                        action='store',
                        dest='channel_parameters',
                        type=float,
                        help='Channel parameters for computing LLR. Required when \
                        channel is bsc or awgn. For bsc, this is the bit flip probability. \
                        For awgn, this is the standard deviation of the Gaussian noise.')
    parser.add_argument('--max-iterations',
                        action='store',
                        dest='max_iterations',
                        type=int,
                        help='Maximum number of decoding iterations for \
                        LDPC belief propagation decoding [default = 100].',
                        default=100)
    return parser


def compute_llr(value, channel_name, channel_value):
    if channel_name == 'bsc':
        if value == 1:
            return -math.log((1 - channel_value) / channel_value)
        elif value == 0:
            return math.log((1 - channel_value) / channel_value)
        else:
            raise RuntimeError("Invalid value encountered for BSC.")
    elif channel_name == 'awgn':
        return -2 * value / (channel_value * channel_value)
    elif channel_name == 'misc':
        return value  # in this case, the values themselves are LLRs
    else:
        raise RuntimeError("invalid channel type")


def main():
    parser = get_parser()
    args = parser.parse_args()
    received_file = args.received_file
    channel_name = args.channel

    if channel_name in ['bsc', 'awgn']:
        if args.channel_parameters is None:
            raise RuntimeError("Channel parameter not specified for bsc/awgn")
        channel_value = args.channel_parameters

    else:
        channel_value = 0.0  # arbitrary value for misc channel for uniform interface

    ldpc_decode_iterations = args.max_iterations
    assert ldpc_decode_iterations > 0

    decoded_file = args.output_file
    pchk_file = args.pchk_file
    transmitted_bits_file = pchk_file + ".transmitted"

    # get path to LDPC library decode script
    ldpc_library_path = os.path.join(os.path.dirname(__file__), os.path.pardir, 'LDPC-codes')
    ldpc_decode_path = os.path.join(ldpc_library_path, 'decode')

    if not os.path.exists(transmitted_bits_file):
        print("INFO: No .transmitted file found. Assuming no puncturing.")
        subprocess.run(ldpc_decode_path + ' ' + pchk_file + ' ' + received_file + ' ' + \
                       decoded_file + ' ' + channel_name + ' ' + str(channel_value) + \
                       ' prprp ' + str(ldpc_decode_iterations), shell=True)
    else:
        print("INFO: Using puncturing.")
        # first load the transmitted bit information
        with open(transmitted_bits_file) as f:
            line1 = f.readline().rstrip('\n')
            num_total_bits = int(line1.split(' ')[-1])
            line2 = f.readline().rstrip('\n')
            transmitted_bits = [int(i) for i in line2.split(' ')]
            # sort for convenience
            transmitted_bits.sort()
            num_transmitted_bits = len(transmitted_bits)

        # To handle puncturing, we compute the LLRs for the received messages.
        # An LLR of 0.0 denotes a punctured bits. This new
        # "received message" is decoded with the misc channel mode in the ldpc
        # library that can handle LLRs.

        # first create a temporary file to store the LLRs for decoding.
        with tempfile.NamedTemporaryFile(mode='w', delete=False, dir=os.getcwd()) as f:
            tmpfilename = f.name
            # now read the received_file line by line and put in LLRs
            with open(received_file) as fin:
                for line in fin:
                    line = line.rstrip('\n')
                    if channel_name == 'bsc':
                        # first remove all spaces (to handle case where bits might be written with or without spaces)
                        line.replace(' ', '')
                        # now read bits
                        received_vals = [int(character) for character in line]
                    else:
                        # read as floats
                        received_vals = [float(val) for val in line.strip(' ').split(' ')]
                    assert len(received_vals) == num_transmitted_bits
                    # now created llr list
                    llr_list = []
                    for i, transmitted_bit in enumerate(transmitted_bits):
                        # first pad llr_list with 0s up to this point
                        llr_list += [0.0] * (transmitted_bit - len(llr_list))
                        llr_list.append(compute_llr(received_vals[i], channel_name, channel_value))
                    # at the end pad till num_total_bits
                    assert len(llr_list) <= num_total_bits
                    llr_list += [0.0] * (num_total_bits - len(llr_list))
                    # now write llr list to file
                    f.write(' '.join([str(llr) for llr in llr_list]) + '\n')

        # now run the decoder with misc 0.0 mode that handles llrs
        subprocess.run(ldpc_decode_path + ' ' + pchk_file + ' ' + tmpfilename + ' ' + \
                       decoded_file + ' misc 0.0 prprp ' + str(ldpc_decode_iterations), shell=True)

        # next we need to take in the decoded output and extract the transmitted bits
        # we reuse the temporary file for this purpose
        with open(tmpfilename, 'w') as f:
            with open(decoded_file) as fin:
                for line in fin:
                    line = line.rstrip('\n')
                    assert len(line) == num_total_bits
                    extracted_transmitted_bits = ''.join([line[i] for i in transmitted_bits])
                    f.write(extracted_transmitted_bits + '\n')

        # move tmpfilename to decoded_file
        os.replace(decoded_file,decoded_file+'.unpunctured')
        os.replace(tmpfilename, decoded_file)
        # We are done!


if __name__ == "__main__":
    main()
