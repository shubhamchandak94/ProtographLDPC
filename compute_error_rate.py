import sys

if len(sys.argv) != 3:
    print("Usage: python3 compute_error_rate.py encoded_file decoded_file")
    sys.exit(1)

encoded_file = sys.argv[1]
decoded_file = sys.argv[2]

with open(encoded_file) as f:
    encoded_codewords = [l.rstrip('\n') for l in f.readlines()]

with open(decoded_file) as f:
    decoded_codewords = [l.rstrip('\n') for l in f.readlines()]

assert len(encoded_codewords) == len(decoded_codewords)
len_codeword = len(encoded_codewords[0])
for i in range(len(encoded_codewords)):
    assert len(encoded_codewords[i]) == len_codeword
    assert len(decoded_codewords[i]) == len_codeword

print('Number of codewords:', len(decoded_codewords))
print('Codeword length:', len_codeword)
bit_errors_total = 0
block_errors_total = 0
total_length = 0
for encoded_codeword, decoded_codeword in zip(encoded_codewords,decoded_codewords):
    bit_errors = sum([encoded_codeword[i] != decoded_codeword[i] for i in range(len(decoded_codeword))])
    if bit_errors != 0:
        block_errors_total += 1
    bit_errors_total += bit_errors
    total_length += len(decoded_codeword)

print('Bit error rate:','%.2f%%'%((bit_errors_total/total_length)*100))
print('Block error rate:','%.2f%%'%((block_errors_total/len(decoded_codewords))*100))
