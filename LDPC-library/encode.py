import subprocess
import os
import argparse
import tempfile


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
    parser.add_argument('--gen-file', '-g',
                        action='store',
                        dest='gen_file',
                        type=str,
                        help='Generator matrix file. Required for encoding.',
                        required=True)
    parser.add_argument('--input-file', '-i',
                        action='store',
                        dest='input_file',
                        type=str,
                        help='Input file containing one or more message blocks (one per line).',
                        required=True)
    parser.add_argument('--output-file', '-o',
                        action='store',
                        dest='output_file',
                        type=str,
                        help='Output file to store encoded blocks (one per line). \
                        An additional output_file.unpunctured is generated when puncturing is used \
                        and contains all the codeword bits including unpunctured bits, to enable easy \
                        extraction of message bits from the codeword.',',
                        required=True)
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    pchk_file = args.pchk_file
    transmitted_bits_file = pchk_file + ".transmitted"
    gen_file = args.gen_file
    src_file = args.input_file
    out_path = args.output_file

    # get path to LDPC library encode script
    ldpc_library_path = os.path.join(os.path.dirname(__file__), os.path.pardir, 'LDPC-codes')
    ldpc_encode_path = os.path.join(ldpc_library_path, 'encode')

    # first perform the encoding
    subprocess.run(ldpc_encode_path + ' ' + pchk_file + ' ' + gen_file +
                   ' ' + src_file + ' ' + out_path, shell=True)

    if not os.path.exists(transmitted_bits_file):
        print("INFO: No .transmitted file found. Assuming no puncturing.")
    else:
        print("INFO: Performing puncturing.")
        # we need to perform puncturing, i.e., remove the untransmitted bits
        # first load the transmitted bit information
        with open(transmitted_bits_file) as f:
            line1 = f.readline().rstrip('\n')
            num_total_bits = int(line1.split(' ')[-1])  # this is the total bit count line
            line2 = f.readline().rstrip('\n')
            transmitted_bits = [int(i) for i in line2.split(' ')]
            # sort for convenience
            transmitted_bits.sort()

        # we will write the punctured codewords to a temporary file first
        with tempfile.NamedTemporaryFile(mode='w', delete=False, dir=os.getcwd()) as f:
            tmpfilename = f.name
            with open(out_path) as fin:
                for line in fin:
                    line = line.rstrip('\n')
                    assert len(line) == num_total_bits
                    extracted_transmitted_bits = ''.join([line[i] for i in transmitted_bits])
                    f.write(extracted_transmitted_bits + '\n')

        # write punctured data from tempfile to output path
        os.replace(out_path,out_path+'.unpunctured')
        os.replace(tmpfilename, out_path)



if __name__ == '__main__':
    main()
