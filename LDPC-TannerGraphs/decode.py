import sys
import os

import math

# input: received message (1 or more codewords)
# channel parameters: bsc error-probability, awgn standard-deviation, misc 0.0
# number of LDPC iterations
# decoded file
# pchk type (regular | protograph)
# parity-check dir

received_codewords = open(sys.argv[1], 'r').read().split('\n')
channel_name = sys.argv[2]
channel_value = int(sys.argv[3])
ldpc_decode_iterations = int(sys.argv[4])
decoded_file = sys.argv[5]

ldpc_type = sys.argv[6]
pchk_file = open(sys.argv[7])

def compute_llr(value, channel_name, channel_value):
    if channel_name == 'bsc':
        if value == 1:
            return math.log((1 - channel_value) / channel_value)
        elif value == 0:
            return -math.log((1 - channel_value) / channel_value)
    elif channel_name == 'awgn':
        return 2 * value / (channel_value * channel_value)
    elif channel_name == 'misc':
        return value  # 0s are given an llr of 0 because erasures are counted as 0s
    else:
        print("invalid channel type")


try:
    transmitted_meta = open(os.path.join(sys.argv[6], '.transmitted')).read().split('\n')  # adapt this for regular codes

    transmitted_bits = transmitted_meta[2].split(' ')
    transmitted_bits = [int(i) for i in transmitted_bits]

    num_bits = transmitted_meta[1].split(' ')
    num_bits = int(num_bits[len(num_bits) - 1])


    llrs = []
    for codeword in received_codewords:
        relative_llrs = []

        codeword_bit = 0
        for bit in range(num_bits):  # loop until the maximum codeword index
            if bit in transmitted_bits:
                relative_llrs.append(compute_llr(int(codeword[codeword_bit]), channel_name, channel_value))
                codeword_bit += 1
            else:
                relative_llrs.append(0)

        llrs.append(relative_llrs)


except FileNotFoundError:
    print("could not find transmission metadata. Either create custom .transmitted or regenerate parity check file")
    exit()
